#!/usr/bin/env python3
"""Post-edit verifier for milvus-docs changes.

Complements ``node check-link.js`` with checks CI does not run, scoped to the
files this session changed: uncommitted working-tree changes (from
``git status --porcelain``), plus — with ``--diff <rev>`` — committed changes
against ``<rev>`` (e.g. the base version branch). With nothing to check the
run exits non-zero instead of printing a vacuous OK:

1. menuStructure en.json (only when it was changed):
   - parses as JSON
   - every node has label / id / order / children
   - ids unique across the tree
   - order values are integers, unique within each sibling group
   Issues are compared against the --base revision (default: the --diff
   revision when given, else HEAD): failures that already exist at --base are
   reported as PRE-EXISTING warnings and do not fail the run; only
   newly-introduced issues exit non-zero.
2. changed markdown pages under site/en/ (fragments/ and template/ excluded):
   must carry front matter whose ``id`` equals the filename.
3. NEW pages (untracked) under site/en/integrations/ or site/en/tutorials/
   whose id appears in the menu: must also be referenced in the matching
   overview table (integrations_overview.md / tutorials-overview.md).
4. timeless-writing check on the ADDED lines of changed pages (whole file for
   new pages): writing-time self-reference ("when this page was written"),
   release-status narration ("pending release", "not yet released",
   "expected in v3.0.3") and future-release phrasing fail the run; rot-prone
   words ("currently", "recently", "the latest version", ...) are reported as
   warnings. Front matter, fenced code blocks, and HTML comments are exempt —
   a TODO comment may say "not yet released"; the prose may not.

Run from the repository root before committing, or with ``--diff <rev>``
after committing.
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


def changed_files(diff_rev=None):
    """Return (changed, untracked) path sets from git status, plus committed
    changes against diff_rev (three-dot) when given."""
    changed, untracked = set(), set()
    for line in git("status", "--porcelain").splitlines():
        if len(line) < 4:
            continue
        st, path = line[:2], line[3:].strip('"')
        if path.endswith("/"):
            continue
        untracked.add(path) if st.strip() == "??" else changed.add(path)
    if diff_rev:
        for line in git("diff", "--name-only", f"{diff_rev}...HEAD").splitlines():
            path = line.strip().strip('"')
            if path and not path.endswith("/"):
                changed.add(path)
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


# Prose that goes stale the day a tag lands (see "Timeless writing" in
# references/doc-standards.md). The blocking tier is high-precision narration;
# the warning tier is softer phrasing that deserves a look.
TIMELESS_BLOCKING = [
    (re.compile(r"when this (?:page|document|doc|guide|section) was written"), "writing-time self-reference"),
    (re.compile(r"at the time of (?:this )?writing"), "writing-time self-reference"),
    (re.compile(r"as of (?:this )?writing"), "writing-time self-reference"),
    (re.compile(r"pending release"), "release-status narration"),
    (re.compile(r"not yet (?:been )?(?:released|shipped|published|generally available)"), "release-status narration"),
    (re.compile(r"expected in (?:pymilvus |milvus |Milvus |PyMilvus )?v?\d"), "release-status narration"),
    (re.compile(r"will (?:be released|ship|become available|land in)"), "future-release narration"),
]
TIMELESS_WARNINGS = [
    (re.compile(r"\bcurrently\b", re.I), '"currently" rots — name the version or behavior instead'),
    (re.compile(r"\b(?:for now|at the moment|right now|as of today)\b", re.I), "time-sensitive phrase — prefer timeless wording"),
    (re.compile(r"\b(?:recently|newly)\b|\ba recent\b", re.I), "relative time — anchor to a version"),
    (re.compile(r"\b(?:upcoming|soon)\b", re.I), "future-event narration"),
    (re.compile(r"\bthe latest version\b", re.I), "unpinned version reference — name the minimum version"),
]


def prose_lines(path):
    """1-based line numbers of prose lines: front matter, fenced code blocks,
    and HTML comments excluded (those may legitimately mention releases)."""
    try:
        lines = open(path, encoding="utf-8").read().splitlines()
    except OSError:
        return set()
    prose, in_front, in_fence, in_comment = set(), False, False, False
    for i, line in enumerate(lines, start=1):
        s = line.strip()
        if i == 1 and s == "---":
            in_front = True
            continue
        if in_front:
            in_front = s != "---"
            continue
        if in_comment:
            if "-->" in s:
                in_comment = False
            continue
        if s.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if "<!--" in s:
            in_comment = "-->" not in s.split("<!--", 1)[1]
            continue
        prose.add(i)
    return prose


def added_lines(base, path):
    """(lineno, text) of lines added in `path` relative to `base`, comparing
    the working tree so pre-commit and post-commit runs behave alike."""
    added, lineno = [], None
    for line in git("diff", "--unified=0", base, "--", path).splitlines():
        if line.startswith("@@"):
            m = re.search(r"\+(\d+)", line)
            lineno = int(m.group(1)) if m else None
        elif lineno is not None and line.startswith("+") and not line.startswith("+++"):
            added.append((lineno, line[1:]))
            lineno += 1
    return added


def check_timeless(pages, untracked, base, errors, warnings):
    """Flag time-sensitive narration on added lines of changed pages."""
    seen = set()
    for p in pages:
        if p in untracked:
            try:
                candidates = list(enumerate(open(p, encoding="utf-8").read().splitlines(), start=1))
            except OSError:
                continue
        else:
            candidates = added_lines(base, p)
        prose = prose_lines(p)
        for lineno, text in candidates:
            if lineno not in prose:
                continue
            for tier, patterns in (("timeless", TIMELESS_BLOCKING), ("timeless-warn", TIMELESS_WARNINGS)):
                for rx, reason in patterns:
                    if rx.search(text) and (p, lineno, tier, reason) not in seen:
                        seen.add((p, lineno, tier, reason))
                        msg = f"{p}:{lineno}: {tier}({reason}): {text.strip()[:120]}"
                        (errors if tier == "timeless" else warnings).append(msg)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--menu", default=MENU)
    ap.add_argument("--diff", default=None, metavar="REV",
                    help="also check changes committed against REV (e.g. origin/v3.0.x); "
                         "without it only uncommitted working-tree changes are checked")
    ap.add_argument("--base", default=None,
                    help="revision to classify pre-existing issues (default: REV of --diff, else HEAD)")
    args = ap.parse_args()

    errors, warnings = [], []
    base = args.base or args.diff or "HEAD"
    changed, untracked = changed_files(args.diff)

    check_menu(changed, base, args.menu, errors, warnings)

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

    check_timeless(pages, untracked, base, errors, warnings)

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
        print(
            "verify.py: FAIL: no changed files to check, so nothing was verified. "
            "Run before committing, or pass --diff <base> (e.g. --diff origin/v3.0.x) "
            "to check committed changes.",
            file=sys.stderr,
        )
        sys.exit(1)
    for w in warnings:
        print(f"verify.py: warning: {w}")
    if errors:
        for e in errors:
            print(f"verify.py: FAIL: {e}", file=sys.stderr)
        sys.exit(1)
    print(f"verify.py: OK (checked {len(pages)} changed page(s), menu changed: {args.menu in changed})")


if __name__ == "__main__":
    main()
