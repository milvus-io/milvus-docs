#!/usr/bin/env python3
"""Surgical editor for site/en/menuStructure/en.json.

Deterministic sidebar operations so agents never hand-edit order values or
JSON syntax. Edits are block-surgical: only the target parent's ``children``
block is rewritten, leaving the rest of the file byte-identical (including
its trailing-whitespace quirks).

Commands:
  show      print the sidebar tree (id, label, order) to locate nodes
  insert    add a page or section under a parent
  move      move an existing node to another parent/position
  remove    remove a node (--force for a section with children)

Orders are bumped, not renumbered: siblings with order >= the new entry's
order shift by +1. Gaps are legal in this corpus and are preserved.

Run from the repository root. Use --dry-run to print a unified diff instead
of writing.
"""

import argparse
import copy
import difflib
import json
import re
import sys

DEFAULT_MENU = "site/en/menuStructure/en.json"


def fail(msg):
    print(f"nav.py: error: {msg}", file=sys.stderr)
    sys.exit(1)


def load_menu(path):
    try:
        raw = open(path, encoding="utf-8").read()
    except OSError as e:
        fail(f"cannot read {path}: {e}")
    try:
        tree = json.loads(raw)
    except json.JSONDecodeError as e:
        fail(f"{path} does not parse: {e}")
    if not isinstance(tree, list):
        fail(f"{path}: top level must be a JSON array")
    return raw, tree


def walk(nodes, path=()):
    """Yield (path_tuple, node) for every node in the tree."""
    for n in nodes:
        yield path, n
        yield from walk(n.get("children", []), path + (n.get("id"),))


def index_tree(tree):
    parents, nodes = {}, {}
    for path, n in walk(tree):
        nid = n.get("id")
        if nid in nodes:
            fail(f"duplicate id in menu: {nid}")
        nodes[nid] = n
        if path:
            parents[nid] = path[-1]
    return nodes, parents


def order_of(node, ctx):
    o = node.get("order")
    if not isinstance(o, int) or isinstance(o, bool):
        fail(f"non-integer order {o!r} on {node.get('id')!r} ({ctx}); fix it manually first")
    return o


def check_entry_id(new_id, nodes):
    if new_id in nodes:
        fail(f"id already exists in the menu: {new_id}")


def resolve_parent(args, nodes):
    parent = nodes.get(args.parent)
    if parent is None:
        fail(f"parent id not found: {args.parent} (run `show` to list ids)")
    if not parent.get("isMenu") and not parent.get("children"):
        fail(f"parent {args.parent} looks like a page (no isMenu, empty children)")
    return parent


def place(children, entry, args):
    """Insert entry into a children list copy and bump colliding orders."""
    kids = list(children)
    if args.after or args.before:
        ref = args.after or args.before
        idx = next((i for i, c in enumerate(kids) if c.get("id") == ref), None)
        if idx is None:
            fail(f"{ref!r} is not a child of the given parent")
        base = order_of(kids[idx], f"sibling {ref}")
        if args.after:
            pos = idx + 1
            entry["order"] = base + 1
        else:
            pos = idx
            entry["order"] = base
    elif args.position is not None:
        pos = args.position
        entry["order"] = args.position
    else:
        pos = len(kids)
        entry["order"] = max((order_of(c, c.get("id")) for c in kids), default=-1) + 1
    entry_order = entry["order"]
    for c in kids:
        if order_of(c, c.get("id")) >= entry_order:
            c["order"] += 1
    kids.insert(pos, entry)
    return kids


# --- block-surgical raw-text rewriting -------------------------------------


def find_children_span(raw, parent_id):
    """Return (start, end) character offsets of the parent's children array
    (from the opening '[' to its matching ']') in the raw text."""
    id_re = re.compile(r'^(\s*)"id":\s*"%s"\s*,?\s*$' % re.escape(parent_id), re.M)
    m = id_re.search(raw)
    if not m:
        fail(f"cannot locate node {parent_id!r} in raw text")
    key = re.compile(r'^ *"children": \[', re.M)
    km = key.search(raw, m.end())
    if not km:
        fail(f"cannot locate children array of {parent_id!r}")
    start = km.end() - 1  # position of '['
    depth, i, in_str, esc = 0, start, False, False
    while i < len(raw):
        ch = raw[i]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
        elif ch == '"':
            in_str = True
        elif ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                return start, i + 1
        i += 1
    fail("unbalanced brackets while scanning children array")


def rewrite_children(raw, parent_id, new_children):
    """Replace the parent's children array in raw, preserving all other bytes."""
    start, end = find_children_span(raw, parent_id)
    indent = re.match(r"^ *", raw[raw.rfind("\n", 0, start) + 1:]).group(0)
    dumped = json.dumps(new_children, indent=2, ensure_ascii=False)
    lines = dumped.split("\n")
    # dump's inner lines already carry one indent level (2 spaces) for objects
    inner = [indent + ln for ln in lines[1:-1]]
    block = "[]" if not inner else "[\n" + "\n".join(inner) + "\n" + indent + "]"
    return raw[:start] + block + raw[end:]


def apply_edit(menu_path, raw, tree, edits):
    """edits: list of (parent_id, new_children). Mutates `tree` in sync.
    Returns the new raw text after sanity checks."""
    new_raw = raw
    for parent_id, new_children in edits:
        new_raw = rewrite_children(new_raw, parent_id, new_children)
    try:
        reparsed = json.loads(new_raw)
    except json.JSONDecodeError as e:
        fail(f"internal error: rewrite produced invalid JSON: {e}")
    expected = copy.deepcopy(tree)
    by_id = {n.get("id"): n for _, n in walk(expected)}
    for parent_id, new_children in edits:
        by_id[parent_id]["children"] = new_children
    if reparsed != expected:
        fail("internal error: rewrite changed the structure unexpectedly; aborting")
    return new_raw


def write_or_diff(menu_path, raw, new_raw, dry_run):
    if new_raw == raw:
        print("no changes")
        return
    if dry_run:
        diff = difflib.unified_diff(
            raw.splitlines(keepends=True), new_raw.splitlines(keepends=True),
            fromfile=f"a/{menu_path}", tofile=f"b/{menu_path}")
        sys.stdout.writelines(diff)
    else:
        with open(menu_path, "w", encoding="utf-8") as f:
            f.write(new_raw)
        print(f"updated {menu_path}")


# --- commands ---------------------------------------------------------------


def cmd_show(args):
    _, tree = load_menu(args.menu)
    for path, n in walk(tree):
        depth = len(path)
        mark = " [section]" if n.get("isMenu") else ""
        line = f"{'  ' * depth}{n.get('order')}\t{n.get('id')}\t{n.get('label')}{mark}"
        if args.match and args.match.lower() not in line.lower():
            continue
        print(line)


def cmd_insert(args):
    raw, tree = load_menu(args.menu)
    nodes, _ = index_tree(tree)
    resolve_parent(args, nodes)
    if bool(args.file) == bool(args.section):
        fail("exactly one of --file or --section is required")
    if args.file:
        check_entry_id(args.file, nodes)
        if not args.file.endswith(".md"):
            fail(f"--file must be a markdown filename ending in .md: {args.file}")
        entry = {"label": args.label, "id": args.file, "order": 0, "children": []}
    else:
        check_entry_id(args.section, nodes)
        entry = {"label": args.label, "id": args.section, "isMenu": True, "order": 0, "children": []}
    parent = nodes[args.parent]
    new_children = place(parent.get("children", []), entry, args)
    new_raw = apply_edit(args.menu, raw, tree, [(args.parent, new_children)])
    write_or_diff(args.menu, raw, new_raw, args.dry_run)


def cmd_move(args):
    raw, tree = load_menu(args.menu)
    nodes, parents = index_tree(tree)
    if args.node not in nodes:
        fail(f"node id not found: {args.node}")
    resolve_parent(args, nodes)
    old_parent_id = parents.get(args.node)
    if old_parent_id is None:
        fail("cannot move a top-level section (edit it manually)")
    if args.parent == old_parent_id and not (args.after or args.before or args.position is not None):
        fail("node is already in that parent; give --after/--before/--position")
    entry = nodes[args.node]
    old_children = [c for c in nodes[old_parent_id]["children"] if c is not entry]
    new_children = place(nodes[args.parent].get("children", []), copy.deepcopy(entry), args)
    edits = [(old_parent_id, old_children), (args.parent, new_children)]
    new_raw = apply_edit(args.menu, raw, tree, edits)
    write_or_diff(args.menu, raw, new_raw, args.dry_run)


def cmd_remove(args):
    raw, tree = load_menu(args.menu)
    nodes, parents = index_tree(tree)
    if args.node not in nodes:
        fail(f"node id not found: {args.node}")
    entry = nodes[args.node]
    if entry.get("children") and not args.force:
        fail(f"{args.node} has {len(entry['children'])} children; use --force to remove the whole subtree")
    parent_id = parents.get(args.node)
    if parent_id is None:
        fail("cannot remove a top-level section (edit the file manually)")
    new_children = [c for c in nodes[parent_id]["children"] if c is not entry]
    new_raw = apply_edit(args.menu, raw, tree, [(parent_id, new_children)])
    write_or_diff(args.menu, raw, new_raw, args.dry_run)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--menu", default=DEFAULT_MENU, help="menu json path (default: %(default)s)")
    common.add_argument("--dry-run", action="store_true", help="print a unified diff instead of writing")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("show", parents=[common], help="list the tree: order, id, label")
    p.add_argument("--match", help="only print lines containing this substring")
    p.set_defaults(func=cmd_show)

    p = sub.add_parser("insert", parents=[common], help="insert a page or section")
    p.add_argument("--file", help="page markdown filename incl. .md (its menu id)")
    p.add_argument("--section", help="new section slug (no .md)")
    p.add_argument("--label", required=True, help="sidebar label")
    p.add_argument("--parent", required=True, help="parent section id")
    g = p.add_mutually_exclusive_group()
    g.add_argument("--after", help="place after this sibling id")
    g.add_argument("--before", help="place before this sibling id")
    g.add_argument("--position", type=int, help="0-based position/order among siblings")
    p.set_defaults(func=cmd_insert)

    p = sub.add_parser("move", parents=[common], help="move a node to another parent/position")
    p.add_argument("--node", required=True)
    p.add_argument("--parent", required=True)
    g = p.add_mutually_exclusive_group()
    g.add_argument("--after")
    g.add_argument("--before")
    g.add_argument("--position", type=int)
    p.set_defaults(func=cmd_move)

    p = sub.add_parser("remove", parents=[common], help="remove a node from the sidebar")
    p.add_argument("--node", required=True)
    p.add_argument("--force", action="store_true", help="remove a section together with its children")
    p.set_defaults(func=cmd_remove)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
