---
name: handoff-from-diff
description: Write HANDOFF.md for the last commit, using only its diff.
argument-hint: "[folder]"
disable-model-invocation: true
allowed-tools: Bash(git log *) Bash(git diff *)
---

# Handoff from the diff

## Context
- Last commit: !`git log -1 --oneline`
- Files changed:
!`git diff HEAD~1 --stat`

## Body
1. Run `git diff HEAD~1 -- $ARGUMENTS` and read the whole diff.
2. Write HANDOFF.md in the folder $ARGUMENTS (or the current folder
   if none was given) with these sections:
   What changed (3 bullets at most), Why, Risk and how to roll back,
   Watch-outs for the next engineer (specific to this code).
3. At most 40 lines. Every claim must be checkable in the diff or the
   current code. If the diff doesn't say why, write "Why: unknown, ask
   the author" rather than guessing.
4. Don't edit any other file.
