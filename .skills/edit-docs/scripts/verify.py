#!/usr/bin/env python3
"""Post-edit verifier for milvus-docs changes.

Complements ``node check-link.js`` with checks CI does not run, scoped to the
files this session changed (tracked-modified plus untracked, from
``git status --porcelain``):

1. menuStructure en.json (only when it was changed):
   - parses as JSON
   - every node has label / id / order / children
   - ids unique across the tree
   - order values are integers, unique within each sibling group
   Issues are compared against the --base revision (default HEAD): failures
   that already exist at --base are reported as PRE-EXISTING warnings and do
   not fail the run; only newly-introduced issues exit non-zero.
2. changed markdown pages under site/en/ (fragments/ and template/ excluded):
   must carry front matter whose ``id`` equals the filename.
3. NEW pages (untracked) under site/en/integrations/ or site/en/tutorials/
   whose id appears in the menu: must also be referenced in the matching
   overview table (integrations_overview.md / tutorials-overview.md).

Run from the repository root before committing.
"""

import argparse
import json
import re
import subprocess
import sys
from collections import Counter

MENU = "site/en/menuStructure/en.json"
OVERVIEWS = {
    "site/en/integrations/": "site/en/integrations/integrations_overview.md",
    "site/en/tutorials/": "site/en/tutorials/tutorials-overview.md",
}
EXCLUDED_DIRS = ("site/en/fragments/", "site/en/template/")


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True).stdout


def changed_files():
    """Return (changed, untracked) path sets from git status."""
    changed, untracked = set(), set()
    for line in git("status", "--porcelain").splitlines():
        if len(line) < 4:
            continue
        st, path = line[:2], line[3:].strip('"')
        if path.endswith("/"):
            continue
        untracked.add(path) if st.strip() == "??" else changed.add(path)
    return changed, untracked


def menu_issues(tree_or_err, prefix=""):
    """Structural issues of a parsed menu tree (or a parse error)."""
    if isinstance(tree_or_err, str):
        return {f"{prefix}parse-error"}
    issues = set()

    def walk(nodes, parent_path):
        ids = [n.get("id") for n in nodes]
        for nid, cnt in Counter(ids).items():
            if cnt > 1:
                issues.add(f"{prefix}dup-id:{nid}")
        orders = []
        for n in nodes:
            nid = n.get("id")
            for key in ("label", "id", "order", "children"):
                if key not in n:
                    issues.add(f"{prefix}missing-key:{nid}:{key}")
            o = n.get("order")
            if not isinstance(o, int) or isinstance(o, bool):
                issues.add(f"{prefix}non-int-order:{nid}")
            else:
                orders.append(o)
        for o, cnt in Counter(orders).items():
            if cnt > 1:
                issues.add(f"{prefix}dup-order:{parent_path}:{o}")
        for n in nodes:
            kids = n.get("children")
            if kids is None:
                continue
            walk(kids, f"{parent_path}/{n.get('id')}")

    walk(tree_or_err, "")
    return issues


def parse_menu(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        return f"parse error: {e}"


def check_menu(changed, base, menu_path, errors, warnings):
    if menu_path not in changed:
        return
    cur = parse_menu(open(menu_path, encoding="utf-8").read())
    base_text = git("show", f"{base}:{menu_path}")
    base_tree = parse_menu(base_text) if base_text else None
    cur_issues = menu_issues(cur)
    base_issues = menu_issues(base_tree) if base_tree is not None else set()
    for i in sorted(cur_issues - base_issues):
        errors.append(f"{menu_path}: {i}")
    for i in sorted(cur_issues & base_issues):
        warnings.append(f"{menu_path}: PRE-EXISTING (also at {base}): {i}")
    if isinstance(cur, str):
        errors.append(f"{menu_path}: {cur}")


def frontmatter_id(path):
    try:
        text = open(path, encoding="utf-8").read()
    except OSError as e:
        return f"<unreadable: {e}>"
    m = re.match(r"\A---\s*\n(.*?)\n---", text, re.S)
    if not m:
        return None
    idm = re.search(r"^id:\s*[\"']?(.+?)[\"']?\s*$", m.group(1), re.M)
    return idm.group(1).strip() if idm else None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--menu", default=MENU)
    ap.add_argument("--base", default="HEAD", help="revision to classify pre-existing issues (default: HEAD)")
    args = ap.parse_args()

    errors, warnings = [], []
    changed, untracked = changed_files()

    check_menu(changed, args.base, args.menu, errors, warnings)

    pages = sorted(
        p for p in (changed | untracked)
        if p.startswith("site/en/") and p.endswith(".md")
        and not p.startswith(EXCLUDED_DIRS)
    )
    for p in pages:
        fid = frontmatter_id(p)
        name = p.rsplit("/", 1)[-1]
        if fid is None:
            errors.append(f"{p}: missing front matter or missing 'id' field")
        elif fid != name:
            errors.append(f"{p}: front matter id {fid!r} != filename {name!r}")

    if untracked:
        menu_text = open(args.menu, encoding="utf-8").read()
        for p in sorted(untracked):
            for prefix, overview in OVERVIEWS.items():
                if not p.startswith(prefix) or not p.endswith(".md"):
                    continue
                name = p.rsplit("/", 1)[-1]
                if name not in menu_text:
                    continue
                if name not in open(overview, encoding="utf-8").read():
                    errors.append(f"{p}: new page is in the menu but missing from {overview}")

    if not (changed | untracked):
        print("verify.py: no changed files to check")
    for w in warnings:
        print(f"verify.py: warning: {w}")
    if errors:
        for e in errors:
            print(f"verify.py: FAIL: {e}", file=sys.stderr)
        sys.exit(1)
    print(f"verify.py: OK (checked {len(pages)} changed page(s), menu changed: {args.menu in changed})")


if __name__ == "__main__":
    main()
