# milvus-io/milvus-docs

## Repository purpose

This repository is the **English documentation source for Milvus**. It holds
the technical user-guide markdown (`site/en/`) that is converted and published
to the `milvus-io/web-content` repo (which in turn feeds the `milvus.io` site
build). Each **branch is one Milvus release line** (`v3.0.x`, `v2.6.x`, ...);
push to a version branch triggers `.github/workflows/ci.yml` to convert the
docs and force-push them to web-content's corresponding version folder.

## Layout

- `site/en/` — English doc source (userGuide, adminGuide, reference, about,
  tutorials, etc.), one checkout per release branch.
- `site/en/Variables.json` — variables referenced in pages/fragments.
- `scripts/` — internal tooling (Feishu doc fetch/report, mdx parsing).
- `.skills/update-user-guide-snippet/` — agent skill for keeping the multi-SDK
  code snippets in `site/en/userGuide/` correct against each SDK's latest API.
  Mirrored by symlink into `.opencode/`, `.claude/`, and `.codex/` so every
  agent tool discovers it.

## Skill usage

When the user asks to **update, fix, or check the code snippets in the Milvus
user guide**, load the `update-user-guide-snippet` skill. Canonical files live
in `.skills/update-user-guide-snippet/` (`SKILL.md` + `references/` +
`scripts/`), mirrored by symlink into `.opencode/`, `.claude/`, and `.codex/`.

Key points:

- The user guide is versioned by **Milvus major version**, where the version is
  the **git branch**: `v3.0.x` → `site/en/userGuide/` (Milvus 3.0), `v2.6.x` →
  `site/en/userGuide/` (Milvus 2.6), etc. There is no `<version>/` prefix in
  paths here.
- Without a version, the skill updates only the **latest major version line**
  (currently `v3.0.x`). Naming a version (e.g. "更新2.6的user guide脚本")
  means switching to that branch first.
- Snippet language mapping: `python` = pymilvus (baseline), `java` =
  milvus-sdk-java, `javascript` = milvus-sdk-node, `go` = milvus-sdk-go, `cpp` =
  milvus-sdk-cpp, `bash` = REST (kept, not an SDK).
- Push/PR behavior: only when the user explicitly asks ("commit and push to the
  remote" / "提交到远程仓库", or "open a PR" / "提交 PR"); branch
  `docs/user-guide-snippets` off the target version branch, one **signed**
  commit.

## Agent rules

- Commit with `git commit -s` so every commit carries a `Signed-off-by:` trailer
  (GitHub DCO).
- In milvus-organization repositories, **each PR must contain exactly one commit**
  — squash or amend before opening a PR.
- Never commit secrets; `.env` and tool scaffolding are gitignored.
- Write documentation prose following the Google Developer Documentation Style
  Guide.
