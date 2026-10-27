---
name: git-workflow
description: Convert a working-tree diff into atomic Conventional Commits and a mergeable PR description. Output the splitter plan plus the PR body.
---

## Purpose

Take a dirty branch and produce shippable Git artefacts: 3–6 atomic commits with Conventional Commit messages and a PR description a senior engineer would merge as-is.

## When to use

- End of a session where you've shipped multiple logical changes.
- Before pushing AI-generated code to a feature branch.
- When you need to backfill commit hygiene after a long working session.

Skip when: the diff is one tiny logical change. Then it's already one commit.

## Body

1. Capture the staged diff: `git diff --staged > /tmp/diff.patch`.
2. Provide that diff to Claude with the **commit-splitter** instruction:
   - Propose 3–6 atomic commits.
   - Each commit: a Conventional Commit subject (`<type>(<scope>): <summary>`, ≤ 72 chars).
   - Each commit body: 1–3 lines explaining *why* (not what — the diff shows what).
   - List which paths/hunks belong to which commit so the human can split via `git reset` + selective `git add -p`.
3. Apply the splits manually. Verify with `git log --oneline`.
4. Capture the branch diff: `git diff main..HEAD > /tmp/branch.patch`.
5. Provide it with the **PR description** instruction:
   - Sections, in order: Summary (2 sentences) · Why · What changed · How to test · Risk · Rollback.
   - End with a "Reviewer checklist" of 3–5 yes/no items.
   - Cap at 40 lines.

## Inputs

- A working-tree diff (`git diff --staged`).
- A branch diff (`git diff main..HEAD`) — same input or different, both are fine.
- The branch name and target base branch.

## Outputs

Two artefacts:

1. **Splitter plan** — a markdown table of `commit_subject | commit_body | files`.
2. **`pr.md`** — a mergeable PR description ≤ 40 lines.

## Worked example

Input: a branch with three intermixed changes — a new `?q=` search parameter, two seeded bug fixes, and a refactor of the SQL helper.

Splitter output:

| Subject | Body | Files |
|---|---|---|
| `feat(notes): add substring search via ?q=` | "Callers asked for free-text search; OR across title and body keeps the contract simple." | `app.py:list_notes` |
| `fix(notes): return 404 on PATCH for unknown id` | "Caller previously got 200 with stale fields when the row did not exist." | `app.py:update_note` |
| `refactor(notes): extract _execute helper` | "Reduces duplication across three handlers without changing behavior." | `app.py:_execute, list_notes, update_note, delete_note` |

PR description ≤ 40 lines, with all six required sections and a 3-item reviewer checklist.
