---
name: edit-docs
description: Create and edit Milvus documentation pages in the milvus-docs repository and deliver every change through a pull request. Use whenever the user wants to modify, update, fix, rephrase, extend, or restructure an existing documentation page under site/en/, add a new documentation page and place it in the sidebar navigation, or import integration documentation from a milvus-io/bootcamp link (a directory or an .ipynb notebook) as a new or updated page — no matter the phrasing ("update the quickstart page", "fix the install guide", "change the wording on the analyzer page", "add a page about X after the analyzer page", "import https://github.com/milvus-io/bootcamp/tree/master/integration/haystack as a new integration doc", or pastes new content to be added to the docs). Covers frontmatter completion, conforming content to doc standards, menuStructure (en.json) navigation edits, link validation, and PR creation.
---

# Edit Milvus Docs

Handle two kinds of documentation changes in this repository and deliver each one as a pull request:

- **Modify** an existing page — the user names a page and describes what to change.
- **Add** a new page — the user supplies content and says where it belongs in the navigation.
- **Import from bootcamp** — the user supplies a milvus-io/bootcamp link (directory or `.ipynb` notebook), which converts to an integration or tutorial page and routes into modify or add.

Both flows share the same standards, validation, and delivery steps.

## Ground rules

- **Every change lands through a PR.** Never commit to a version branch (`v3.0.x`, `v2.6.x`, ...) directly. Work on a `docs/*` feature branch, make exactly one signed commit, push, and open a PR — see `references/pr-workflow.md`.
- **The git branch is the Milvus version line.** Docs for Milvus 3.0 live on `v3.0.x`, for 2.6 on `v2.6.x`, all under `site/en/` (there is no version prefix in paths). Default to the currently checked-out branch. If the user names a version, switch to that branch first.
- **Docs are English only** and must follow the repo's doc standards. Read `references/doc-standards.md` before writing or reworking any prose.
- **Adapt user-supplied content to the standards; never paste it as-is.** Fix frontmatter, headings, links, code fences, tone, and reuse mechanisms (fragments, variables, image macros), while preserving the author's technical intent. List the adaptations in the PR body so reviewers see them.
- **Ask when a request is genuinely ambiguous; act when it is not.** One precise question beats editing the wrong thing, but do not stall on requests that are already actionable.

## Step 0 — Preflight

1. Confirm the version branch: `git branch --show-current`. Resolve the target version per the ground rules.
2. If the working tree is dirty, stop and ask the user to commit or stash first — doc edits must not mix with unrelated local work.
3. If the tree is clean and the branch tracks a remote, `git pull --ff-only` to start from the latest docs.

## Flow A — Modify an existing page

1. **Locate the page.** The user may give a milvus.io URL (`https://milvus.io/docs/quickstart.md`), a page title ("Quickstart"), or a filename. The URL slug / filename is the markdown filename — find it under `site/en/` with `find site/en -name '<slug>*.md'` or by grepping the title. If nothing matches, search the sidebar labels in `site/en/menuStructure/en.json`; if several pages could match the user's wording, list the candidates and ask which one.
2. **Read the whole page before editing.** Note the conventions already in use — `{{fragments/...}}` includes, `{{var.*}}` variables, `<div class="alert note">` blocks, `<div class="multipleCode">` multi-SDK tabs, image macros — and keep them consistent in your edit.
3. **Clarify if needed.** Ask the user when the change is directional but underspecified ("make this clearer"), two sections could be the target, the request conflicts with the page's structure, or version-specific behavior is unclear. Do not ask when the request is concrete — just edit.
4. **Apply the change** per `references/doc-standards.md`, touching the minimum needed. If you change the page `title`, also update the matching `label` in `en.json`. Keep the edit scoped; unrelated rewrites invite review friction.
5. **Validate and deliver** (below).

## Flow B — Add a new page

1. **Resolve the placement.** The user supplies content and a location, usually a parent section plus a neighbor ("under User Guide, after the analyzer page"). Map it to an exact node in `site/en/menuStructure/en.json` — read `references/menu-structure.md` first for the schema, and use `python3 .skills/edit-docs/scripts/nav.py show --match <text>` to locate parent/neighbor ids. If the parent section is not stated, infer candidates from the content and confirm with the user before inserting. If the stated neighbor cannot be found, ask rather than guessing a spot.
2. **Create the file.** The path mirrors the section's directory under `site/en/` (e.g. `site/en/userGuide/<name>.md`). Name it lowercase and brief, hyphen-separated for new pages (`analyzer-overview.md`); when adding into an older section whose files use underscores, match the neighbors.
3. **Complete the frontmatter.** `id` (mandatory — exactly the filename including `.md`), `title` (title case, becomes the h1), `summary` (one sentence, ≤143 characters), and optionally `related_key` / `group`. Field rules live in `references/doc-standards.md`. Frontmatter is never boilerplate; fill it deliberately.
4. **Adapt the content to the standards.** Start from the closest template in `site/template/` (how-to, conceptual, reference, tutorial) and structure the page accordingly; fix headings, links, code fences, and tone per `references/doc-standards.md`. Reuse existing fragments and variables instead of duplicating their content. If the user supplied content in another language, author the page in English.
5. **Insert the page into `en.json`** at the agreed position with `python3 .skills/edit-docs/scripts/nav.py insert` (e.g. `nav.py insert --file <name>.md --label "<Label>" --parent <section> --after <sibling.md>`; it bumps sibling orders and writes only the affected block). Preview with `--dry-run`. Never hand-edit `order` values or JSON by hand; `nav.py move` / `nav.py remove` exist for repositioning.
6. **Validate and deliver** (below).

## Flow C — Import from a bootcamp link

The user supplies a link into the [milvus-io/bootcamp](https://github.com/milvus-io/bootcamp) repository — a notebook file (`/blob/<ref>/<path>.ipynb`) or a directory (`/tree/<ref>/<dir>`) — and states whether it becomes a new integration page or updates an existing one.

1. **Read `references/integration-pages.md` first.** It defines the page anatomy shared by `site/en/integrations/` and `site/en/tutorials/`, the canonical blocks (badges, Colab note, connection note), the `nbconvert` conversion workflow, and the corpus-specific conventions (absolute milvus.io links, overview table rows, sidebar placement).
2. **Fetch and convert.** Download the notebook raw and convert with `jupyter nbconvert --to markdown`, then apply the post-processing checklist from the reference (frontmatter, badges, `shell` fences, alert blocks, artifact cleanup). A directory link may hold several notebooks — list its contents and confirm with the user which to import (one page per notebook) before doing the work.
3. **Route by the user's instruction.** A new page continues with Flow B (steps 2–6, plus the overview table row — `integrations_overview.md` for integrations, `tutorials-overview.md` for tutorials); updating an existing page continues with Flow A, applying the converted content as the edit and keeping the existing filename and `id` even if the notebook name differs. If the user did not say which, and a page for that integration or tutorial already exists, ask.
4. **Validate and deliver** (below).

## Validate and deliver (all flows)

1. **Validate.** From the repo root run `node check-link.js` (run `npm install` once first if `node_modules/` is missing). It enforces that each page's frontmatter `id` equals its filename, that every sidebar `.md` id resolves to a real file, and that inner links are valid. Then run `python3 .skills/edit-docs/scripts/verify.py`, which adds session-scoped checks CI does not have: menu structure issues (duplicate ids/orders, non-integer orders) compared against the base revision (HEAD, or the `--diff` revision when given) so only newly-introduced ones fail, frontmatter presence on changed pages, and the overview-table row for new integration/tutorial pages. Pass `--diff <base>` (e.g. `--diff origin/v3.0.x`) to include changes you have already committed; when there is nothing to check, the run fails loudly instead of printing a vacuous OK. Fix every failure your change caused; failures marked PRE-EXISTING go into the PR body as a note, not a blocker.
2. **Deliver via PR.** Follow `references/pr-workflow.md`: branch `docs/<short-topic>-<version-branch>`, one `git commit -s` commit titled `docs: ...`, push to origin, `gh pr create` against the version branch with the PR body template. Do this without asking — the PR is the required delivery path — unless the user explicitly held it back (a "dry run" / "don't push" request), in which case skip branching and committing and just show the diff.
3. **Report.** Summarize what changed where, give the PR link, and list the adaptations you made to user-supplied content.
