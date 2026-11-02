# Chapter 6: Safe Git Workflows for AI-Assisted Development

Project 6 moves the `claude-code-projects` workspace to GitHub and works on a feature branch: atomic Conventional Commits split from a messy working tree, a pull request description written from the diff, and the `@claude` GitHub Action.

This chapter works on the files you already have from Chapters 1 to 5, so it has no starter files. This folder holds the reference outputs to compare yours against.

| File | What it is | Section |
| --- | --- | --- |
| `pr.md` | Sample pull request description, written from `git log main..HEAD` and `git diff main...HEAD` | Writing the pull request description |
| `claude.yml` | The `@claude` workflow for manual setup. Copy it to `.github/workflows/claude.yml` in your own repository | Adding the @claude GitHub Action |
| `README.md` | This file | Project 6 |

GitHub runs workflows only from `.github/workflows/` at the root of a repository, so `claude.yml` does nothing while it sits in this folder.

If you authenticate with a Claude subscription instead of an API key, replace the last line of `claude.yml` with:

```yaml
          claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
```
