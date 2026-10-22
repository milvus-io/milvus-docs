# PR workflow

Every documentation change ships as a pull request. Never push to a version
branch, never merge your own PR.

## Branch

- Base: the version branch being edited (`v3.0.x`, `v2.6.x`, ...).
- Feature branch: `docs/<short-topic>-<version-branch>` — e.g.
  `docs/tokenizer-split-rules-v3.0.x`. Topic short and lowercase.
- **Branch off the version branch explicitly**, not off HEAD:
  `git checkout -b docs/<topic>-<version-branch> <version-branch>`. This keeps
  unmerged local work on the current checkout from riding into the PR. If the
  working tree already holds edits that belong in this PR, carry them over:
  `git stash push` → create the branch off the version branch → `git stash pop`.

## Commit

- Stage only the files you intentionally changed (doc pages, `en.json`,
  `assets/` if images were added) — review `git status` first; never
  `git add -A` blindly.
- Exactly **one** commit per PR (milvus-org review tooling expects it):

  ```bash
  git commit -s -m "docs: <lowercase imperative summary>"
  ```

  `-s` adds the `Signed-off-by:` trailer required by the DCO check.
- If iteration produces extra commits, squash before pushing:
  `git reset --soft <version-branch> && git commit -s -m "..."`.

## Push and open the PR

```bash
git push -u origin <branch>
gh pr create --base <version-branch> --title "docs: <summary>" --body "$(cat <<'EOF'
## What changed
- ...

## Why
...

## Reviewer notes
- Content adaptations (rework done to meet doc standards): ...
- Validation: `node check-link.js` passed (or: pre-existing failures noted here)

Checklist:
- [ ] Frontmatter complete (`id` = filename, `title`, `summary` ≤143 chars)
- [ ] Sidebar `en.json` updated (page added/renamed/repositioned)
- [ ] `node check-link.js` passes
EOF
)"
```

Report the PR URL to the user together with a summary of the changes and any
adaptations made to their content.

## Hard rules

- One commit, signed; no force-push to shared branches; no direct pushes to
  version branches.
- If `gh` is unavailable or authentication fails, push the branch and give the
  user the compare URL as a fallback:
  `https://github.com/milvus-io/milvus-docs/compare/<version-branch>...<branch>`.
- If the user asked for a dry run ("don't push"), skip this section entirely —
  leave the edits in the working tree and show the diff instead.
