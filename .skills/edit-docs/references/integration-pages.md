# Bootcamp-derived pages: integrations and tutorials

Read this for any change under `site/en/integrations/` or `site/en/tutorials/`
— and always when importing from a
[milvus-io/bootcamp](https://github.com/milvus-io/bootcamp) notebook. Both
corpora are derived from runnable bootcamp notebooks, which gives their pages
a shared anatomy and several verbatim-reused blocks.

## Anatomy of an integration page

1. **Frontmatter** — `id` (= filename), `summary` (one sentence, typically
   "This guide demonstrates how to ... using <Partner> and Milvus."), `title`.
2. **Badge block** — Colab + GitHub badges pointing at the bootcamp notebook
   (canonical HTML below), immediately after the frontmatter.
3. **h1 + intro** — what the guide builds, then 1–2 paragraphs: what the
   partner tool is (with its official link) and what Milvus contributes.
4. **`## Prerequisites`** (sometimes `## Preparation`) — Python version
   requirement, install command in a `shell` fence, the Colab restart note,
   and any API-key environment setup.
5. **Task-oriented h2 sections** from the notebook — a one-or-two-sentence
   lead-in before each code block; keep cell output only when it is
   meaningful, as indented text.
6. **Connection note** — the canonical Milvus connection block (below) right
   after the first Milvus client / document store setup.
7. **`## Conclusion`** — common but not universal; keep when the notebook has
   one, linking onward (partner README, related guides).

## Canonical blocks — reuse verbatim

**Badges** (replace `<bootcamp-blob-url>` with the notebook's `blob/master/`
URL):

```html
<a href="https://colab.research.google.com/github/milvus-io/bootcamp/blob/master/<path>.ipynb" target="_parent">
    <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>
<a href="https://github.com/milvus-io/bootcamp/blob/master/<path>.ipynb" target="_blank">
    <img src="https://img.shields.io/badge/View%20on%20GitHub-555555?style=flat&logo=github&logoColor=white" alt="GitHub Repository"/>
</a>
```

**Colab restart note** (wrap the notebook's blockquote in the alert div):

```html
<div class="alert note">

If you are using Google Colab, to enable dependencies just installed, you may need to **restart the runtime** (click on the "Runtime" menu at the top of the screen, and select "Restart session" from the dropdown menu).

</div>
```

**Connection note** — `MilvusClient` variant:

```html
<div class="alert note">

As for the argument of <code>MilvusClient</code>:
- Setting the <code>uri</code> as a local file, e.g.<code>./milvus.db</code>, is the most convenient method, as it automatically utilizes [Milvus Lite](https://milvus.io/docs/milvus_lite.md) to store all data in this file.
- If you have large scale of data, you can set up a more performant Milvus server on [docker or kubernetes](https://milvus.io/docs/quickstart.md). In this setup, please use the server uri, e.g.<code>http://localhost:19530</code>, as your <code>uri</code>.
- If you want to use [Zilliz Cloud](https://zilliz.com/cloud), the fully managed cloud service for Milvus, adjust the <code>uri</code> and <code>token</code>, which correspond to the [Public Endpoint and Api key](https://docs.zilliz.com/docs/on-zilliz-cloud-console#free-cluster-details) in Zilliz Cloud.

</div>
```

For integration clients that take `connection_args` (e.g. Haystack's
`MilvusDocumentStore`), use the same three bullets with "For the
`connection_args`:" as the lead-in. Inline code spans may stay as
backticks instead of `<code>` — match the existing page.

## Conventions specific to bootcamp-derived pages

- **Links to other Milvus pages are absolute** `https://milvus.io/docs/<slug>.md`
  URLs (used across the whole corpus; zero relative links). This is a
  deliberate exception to the relative-link preference in
  `references/doc-standards.md` — these pages mirror notebooks, and the
  absolute form matches every neighbor page.
- **Install commands**: `shell` fence, `pip install ...` with the notebook's
  `!` magic prefix removed. A `$` prompt prefix appears in parts of the corpus
  (notably `site/en/tutorials/`) — when editing an existing page, match its
  style to minimize the diff.
- **File naming**: default is the notebook basename with `.md`
  (`build_RAG_with_milvus_and_ollama.ipynb` → `build_RAG_with_milvus_and_ollama.md`);
  the user may override (some older docs diverge, e.g.
  `rag_with_milvus_and_haystack.ipynb` → `integrate_with_haystack.md`).

## Sidebar placement

- In `en.json`, the `integrations` section groups pages into category
  subsections (Orchestration, Agents, Embedding Models, LLMs, Evaluation &
  Observability, Knowledge Engineering, Data Sources, Others, after the
  `integrations_overview.md` entry). Infer the category from the partner
  stack and confirm with the user; insert per `references/menu-structure.md`.
- **`integrations_overview.md` must gain a table row** for every new
  integration page:
  `| [<Title>](<file>.md) | <Use Case> | Milvus, <Partner> |`
  (Use Case examples from the existing table: RAG, Semantic Search, Agents,
  Evaluation & Observability, Data Sources, Orchestration).

## Tutorial pages (site/en/tutorials/)

The second bootcamp-derived corpus (~25 pages). Source notebooks live in
bootcamp under `tutorials/` (mostly `tutorials/quickstart/<name>.ipynb`), and
the doc filename mirrors the notebook basename
(`hybrid_search_with_milvus.ipynb` → `hybrid_search_with_milvus.md`).

Everything above applies — same anatomy, canonical blocks, post-processing
checklist — with these placement differences:

- **Sidebar**: the `tutorials` section in `en.json` is a **flat list** (no
  category subsections). Insert per `references/menu-structure.md` at the
  position the user gives; no category decision needed.
- **Overview table**: `tutorials-overview.md` must gain a row, with its own
  column shape: `| [<Title>](<file>.md) | <Use Case> | <Related Milvus Features> |`.
- **Links**: same convention — absolute `https://milvus.io/docs/...` URLs for
  Milvus doc pages; bare filenames for same-directory tutorial siblings.

## Importing from bootcamp — workflow

Accepted inputs:
- **Notebook file**:
  `https://github.com/milvus-io/bootcamp/blob/<ref>/<path>.ipynb`
- **Directory**:
  `https://github.com/milvus-io/bootcamp/tree/<ref>/<dir>` — list its contents
  (`gh api repos/milvus-io/bootcamp/contents/<dir>` or fetch the page) and
  confirm with the user which notebook(s) to import; directories may hold
  several. Bootcamp material can live anywhere in the repo (`integration/`,
  `bootcamp/RAG/`, ...), not only `integration/`.

Steps:

1. **Fetch** the notebook raw:
   `https://raw.githubusercontent.com/milvus-io/bootcamp/<ref>/<path>.ipynb`
2. **Convert** with the maintainer's standard method:
   `jupyter nbconvert <nb>.ipynb --to markdown`. If `jupyter` is unavailable,
   install it (`pip install nbconvert`) or fall back to a small Python pass
   over the notebook JSON (markdown cells → prose, code cells → fences).
3. **Post-process** — the delta between nbconvert output and a published
   page is small and mechanical:
   - Add frontmatter (`id`, `summary`, `title`) — title/summary usually come
     from the notebook's h1 and opening prose.
   - Reformat the badge block onto separate lines (nbconvert mashes the two
     anchors into one line).
   - `! pip install ...` → `pip install ...`; fence tag `python` → `shell`.
   - Wrap the Colab note blockquote in `<div class="alert note">`.
   - Ensure the canonical connection note follows the first Milvus client
     setup; normalize wording to the block above.
   - Remove nbconvert artifacts: execution counts, stray anchors, doubled
     blank lines, and the `<name>_files/` image directory (a genuinely
     needed image goes into `assets/` at the repo root, referenced by
     relative path — see `references/doc-standards.md` §Images; otherwise
     drop it).
   - Cell outputs: keep only meaningful ones as indented text. An unexecuted
     notebook has none — **never fabricate output**; note in the PR body that
     outputs are absent so the maintainer can run the notebook.
   - Milvus doc links become absolute `milvus.io/docs/...` URLs.
   - **Do not regress docs-side improvements.** When the existing page
     contains newer edits made on the docs side (check provenance with
     `git log -- <page>` / `git blame` if unsure), keep them instead of
     overwriting with the notebook's older captured content, and surface the
     deviation to the user. A notebook's captured outputs can be stale. To
     see what changed in the notebook since the last import:
     `gh api "repos/milvus-io/bootcamp/commits?path=<path>&per_page=5"`.
4. **Route by user instruction**: updating an existing page →
   continue with Flow A (keep the existing filename/`id` even if the notebook
   name differs). Creating a new page → continue with Flow B, adding the
   sidebar placement in `en.json` (category subsection for integrations;
   flat list for tutorials) **and** the overview table row
   (`integrations_overview.md` or `tutorials-overview.md`).
