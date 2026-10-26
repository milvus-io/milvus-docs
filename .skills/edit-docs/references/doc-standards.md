# Milvus doc standards

Read this before writing or reworking prose in `site/en/**`. The governing style
reference is the Google Developer Documentation Style Guide (see CONTRIBUTING.md);
this file captures the repo-specific rules and the points that come up most.

## Frontmatter

Every page starts with YAML frontmatter:

```markdown
---
id: quickstart.md
title: Quickstart
summary: Get started with Milvus.
---
```

| Field | Required | Rules |
|---|---|---|
| `id` | yes | Exactly the markdown filename including `.md`. Must be unique across `site/en/`; the sidebar (`en.json`) references pages by this id, and CI (`check-link.js`) rejects any mismatch between `id` and filename. |
| `title` | recommended | Title case. Used as the page h1 — the body must start with a single `# <title>` matching it. |
| `summary` | recommended | One tight sentence; the 143-character target from CONTRIBUTING.md is a guideline, not an enforced rule (sibling pages vary widely in length). It becomes the page's meta description; the page's opening sentence is a good choice. |
| `related_key` | optional | Keyword that pulls related FAQ entries onto the bottom of the page. Set only when the page genuinely matches existing FAQ content. |
| `group` | optional | Id of the group's leading page, when this page is part of a multi-page group (e.g. the Helm install guides under adminGuide). |

Field order is not enforced (`id, summary, title` is common in older files); keep
one field per line.

## File naming

- Lowercase. Hyphens between words for new pages (`analyzer-overview.md`);
  older sections use underscores (`time_sync.md`) — when adding into an older
  section, match the neighbors' style.
- Brief but descriptive: the public URL on milvus.io is derived from it.

## Page structure

- Exactly one h1 (matching `title`), then h2/h3 in order without skipping levels.
- How-to pages: task-oriented h2 headings, prerequisites before steps, steps in
  second-person imperative ("Install Milvus", not "Installing Milvus").
- Conceptual/reference pages: open with a definition or overview before details.
- The opening paragraph (1–3 sentences) says what the page covers and for whom.

## Voice and style

- Present tense, active voice, second person ("you"). No "please", no "we will".
- Title case only for the page title; headings below it, table headers, and UI
  element names use sentence case.
- Link Milvus-specific terms to their concept/reference page on first use rather
  than re-explaining them.
- Introduce every list and table with a sentence ending in a colon; keep list
  items parallel in structure.

## Timeless writing

The docs outlive the release cycle: prose that reads correctly today and
wrongly the day a tag lands is a bug. State facts so they survive releases.

- **Anchor compatibility to minimum versions, not release status:**
  - Good: "The `headers` parameter requires pymilvus v3.0.3 or later on the
    3.x line."
  - Bad: "…was pending release when this page was written." (becomes false the
    day it ships)
  - Bad: "requires a recent pymilvus" (unverifiable).
- **Never narrate the writing moment or the future.** No "at the time of
  writing", "as of this writing", "not yet released", "expected in v3.0.3",
  "will ship in the next release", "upcoming". Unpublished features don't get
  prose: keep the material on a branch, and put the contingency (release PRs,
  expected versions, verify-after-release notes) in an HTML comment
  (`<!-- TODO: … -->`) — comments don't render, so they may say things prose
  may not.
- **Avoid transient-status words in prose**: "currently", "for now",
  "recently", "soon", "the latest version". Name the version or describe the
  behavior instead.
- **Versioned history is fine when the version is the fact**: "Partition Key
  Isolation applies only to HNSW" and "Materialized View is enabled by default
  since 2.5.4" are timeless — they pin behavior to a version, not to the
  calendar.

`verify.py` enforces the mechanical subset on added lines: writing-time
self-reference and release-status narration fail the run; transient-status
words are reported as warnings. Front matter, fenced code blocks, and HTML
comments are exempt.

## Reuse mechanisms — prefer these over duplicating content

- **Fragments** — reusable blocks in `site/en/fragments/`, included with
  `{{fragments/<name>.md}}` (e.g. `{{fragments/multiple_code.md}}`). Before
  copying repeated content (install caveats, FAQ blurbs, tab scaffolds), check
  whether a fragment already covers it.
- **Variables** — `site/en/Variables.json`, referenced as `{{var.<key>}}` in
  prose, links, and code (e.g. `{{var.milvus_release_version}}`). Use variables
  for version numbers and download URLs instead of hardcoding, so a release
  only touches `Variables.json`.
- **Images** — a new image file goes in `assets/` at the repo root and is
  referenced by its path relative to the page
  (`![Alt](../../../../../assets/<file>.png)` — depth depends on the page's
  location; see `membership-match.md` for a current example). Many older
  images are referenced by their S3 URL
  (`https://milvus-docs.s3.us-west-2.amazonaws.com/assets/<file>.png`) —
  when reusing an existing image, keep the form the page's neighbors use.
  Reuse existing images where possible; screenshots must reflect the current
  UI.
- **Alert blocks** — notes/warnings use this exact shape (see any existing page):

  ```html
  <div class="alert note">

  > The note text as a blockquote.

  </div>
  ```

- **Multi-SDK code tabs** — when a section shows the same operation in several
  SDKs, precede the blocks with the tab scaffold:

  ```html
  <div class="multipleCode">
      <a href="#python">Python</a>
      <a href="#java">Java</a>
      <a href="#go">Go</a>
      <a href="#javascript">NodeJS</a>
      <a href="#cpp">C++</a>
      <a href="#bash">cURL</a>
  </div>
  ```

  followed by one fenced code block per language, `python` first (it is the
  baseline the other SDKs mirror), with fence tags matching the hrefs
  (`python`, `java`, `go`, `javascript`, `cpp`, `bash`). Not every page needs
  every language — mirror the page's existing set.

## Links

- Links to pages in this repo/branch are markdown-file references the way
  neighboring pages write them — usually a bare filename relative to the
  page's own directory (`[Analyzer Overview](analyzer-overview.md)`), and
  cross-directory bare filenames also occur and resolve repo-wide in
  `check-link.js`. Some older pages (notably integrations) use absolute
  `https://milvus.io/docs/...` URLs; don't add new ones outside
  `site/en/integrations/`.
- External links are absolute URLs.

## Code blocks

- Always tag the fence with its language; `bash` for shell commands.
- Keep style consistent with the surrounding page (imports, client
  initialization, variable naming) rather than introducing a new style.

## Templates

New pages start from the closest template in `site/template/`:

| Template | Use for |
|---|---|
| `how-to-doc-template.md` | Goal-driven task pages (default for user guide additions) |
| `conceptual-doc-template.md` | Explaining a concept or architecture |
| `reference-doc-template.md` | Lookup material — config tables, API lists |
| `tutorial-doc-template.md` | End-to-end walkthroughs |

## Language

English only — it is the docs' official language. If the user supplies content
in another language, author the English page from it (preserving technical
intent) rather than pasting a literal translation.
