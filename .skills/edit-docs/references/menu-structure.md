# Sidebar: site/en/menuStructure/en.json

The rendered navigation on milvus.io is generated from this file. Adding,
moving, or renaming a page requires an `en.json` edit. (CONTRIBUTING.md
§Sidebar describes the same schema for contributors.)

## Schema

The top level is an array of section nodes; each node has:

```json
{
  "label": "Run Milvus Standalone",
  "id": "run_milvus_docker",
  "order": 2,
  "isMenu": true,
  "children": []
}
```

| Field | Meaning |
|---|---|
| `label` | Sidebar text. May be shorter than the page `title` (e.g. title "Milvus Standalone" → label "Milvus Standalone", but "Docker Compose (Linux)" style suffixes are fine). Match the sibling style. |
| `id` | **Pages:** the filename including `.md`, identical to the page's frontmatter `id`. **Sections:** a short slug without `.md`, underscore-separated (e.g. `run_milvus_docker`). Ids must be unique across the whole tree. |
| `order` | Position among siblings, 0-based. Must be **unique within its sibling group** — duplicates break the sort. Gaps are legal and common (legacy groups have them; the renderer sorts by value), so never renumber a whole group just to close gaps. |
| `isMenu` | `true` for sections that contain children; omitted (or absent) for pages. |
| `children` | Nested nodes; `[]` for pages. |

A page's markdown file usually lives in the directory implied by its parent
section (e.g. children of `run_milvus_docker` sit in `site/en/getstarted/run-milvus-docker/`),
but the tree does not enforce a path mapping — what matters is that the id is
unique and resolves to a real file.

## Insertion, moving, removal — use nav.py

Always use the bundled script instead of editing the JSON by hand; it bumps
sibling orders correctly and rewrites only the affected block, leaving the
rest of the file byte-identical:

```bash
# locate the parent/neighbor ids first
python3 .skills/edit-docs/scripts/nav.py show --match haystack

# insert a page after a sibling (append at end if --after is omitted)
python3 .skills/edit-docs/scripts/nav.py insert \
  --file my-new-page.md --label "My New Page" \
  --parent run_milvus_docker --after install-overview.md --dry-run

# a new subsection instead of a page: --section <slug> (implies isMenu)
python3 .skills/edit-docs/scripts/nav.py insert \
  --section my_section --label "My Section" --parent userguide

python3 .skills/edit-docs/scripts/nav.py move --node my-new-page.md --parent <other> --after <sibling>
python3 .skills/edit-docs/scripts/nav.py remove --node my-new-page.md   # --force drops a section with children
```

A page node is `{label, id, order, children: []}`; a section adds
`"isMenu": true` and an id without `.md`. The script refuses duplicate ids,
unknown parents, and nodes with non-integer order values (fix those
manually first).

The manual fallback (only if the script is unavailable): insert the node
with a `order` one past the anchor sibling, bump every later sibling's
`order` by 1, keep 2-space indentation and the existing key order
(`label`, `id`, `isMenu`, `order`, `children`), and never reformat the
whole file.

## Checks before pushing

- `python3 .skills/edit-docs/scripts/verify.py` — structural checks on the
  changed menu (parse, required keys, duplicate ids, duplicate/non-integer
  orders), classified against `HEAD` so only newly-introduced issues fail.
- `node check-link.js` — fails on duplicate ids anywhere in the tree and on
  any `.md` id that does not resolve to a real markdown file.

## Renames and title changes

- **Title change:** update the page's frontmatter `title` and h1, and update
  the node's `label` to match (labels may stay shorter than titles).
- **File rename:** discouraged unless the user asks. If done, rename the file,
  update its frontmatter `id`, update the node's `id` in `en.json`, and fix
  every relative link pointing at the old name
  (`grep -rl '<old-name>' site/en`).
