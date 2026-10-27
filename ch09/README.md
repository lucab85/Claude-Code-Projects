# Chapter 9: Packaging Your Workflows as Reusable Skills

In this chapter, you package the Notes API smoke test as a skill: a `SKILL.md`
file of instructions plus a bundled script, `smoke.py`, that starts a temporary
copy of the API, runs eight checks and cleans up after itself. You run the
skill by name, let Claude pick it up from a plain question, watch it catch a
planted bug, and then write two more skills in the exercises.

Files under `.claude/` mirror where they go in your `claude-code-projects`
workspace. Copy them to the same path at the workspace root, for example:

```bash
cp -r ch09/.claude/skills/notes-api-smoke ~/claude-code-projects/.claude/skills/
```

## Files

| File | What it is | Section | Copy it to |
|---|---|---|---|
| `.claude/skills/notes-api-smoke/SKILL.md` | The skill's frontmatter and instructions | Writing SKILL.md | `.claude/skills/notes-api-smoke/SKILL.md` |
| `.claude/skills/notes-api-smoke/smoke.py` | The smoke-test script (standard library only) | Writing the smoke-test script | `.claude/skills/notes-api-smoke/smoke.py` |
| `invocation.md` | A recorded run of the skill against `ch05/notes_api.py` | Recording the result and committing | `ch09/invocation.md` (write your own from a real run) |
| `.claude/skills/visual-diff/SKILL.md` | Visual diff skill with named arguments | Exercise 9.1 | `.claude/skills/visual-diff/SKILL.md` |
| `.claude/skills/handoff-from-diff/SKILL.md` | Handoff skill with dynamic context injection | Exercise 9.2 | `.claude/skills/handoff-from-diff/SKILL.md` |
| `solutions/ex9.5/.claude/skills/notes-api-smoke/smoke.py` | `smoke.py` with the extra "search treats % literally" check | Exercise 9.5 | `.claude/skills/notes-api-smoke/smoke.py` (replaces the original) |
| `solutions/ex9.5/.claude/skills/notes-api-smoke/SKILL.md` | `SKILL.md` with Purpose and Worked example updated for nine checks | Exercise 9.5 | `.claude/skills/notes-api-smoke/SKILL.md` (replaces the original) |

The companion skills library used in "Using the companion skills library" and
Exercise 9.3 (`code-review`, `release-notes` and the others) is in the
`skills/` folder at the root of this repository. Install one with, for
example, `cp -r skills/release-notes ~/claude-code-projects/.claude/skills/`.

## How to test

Activate a virtual environment with FastAPI and uvicorn installed (the one
from Chapter 4), then run the script directly from the root of this
repository. It needs no other packages.

```bash
python3 ch09/.claude/skills/notes-api-smoke/smoke.py ch05/notes_api.py
python3 ch09/.claude/skills/notes-api-smoke/smoke.py ch04/winner/notes_api.py
python3 ch09/.claude/skills/notes-api-smoke/smoke.py ch04/candidate-a/notes_api.py
python3 ch09/.claude/skills/notes-api-smoke/smoke.py ch04/candidate-b/app.py
echo $?
```

Expected results (Table 9.5): the first two print `RESULT: PASS` and exit 0.
Candidate A fails only `deleted note is 404`, because its body is
`{"detail": {"error": "not found"}}`. Candidate B fails the blank title, update
(405) and 404-body checks. Both exit 1. The script copies the module into a
temporary folder, so no `notes.db` is created next to your code.

To try the Exercise 9.5 version, run
`ch09/solutions/ex9.5/.claude/skills/notes-api-smoke/smoke.py` the same way:
`ch05/notes_api.py` passes all nine checks, and `ch04/winner/notes_api.py`
fails only `search treats % literally`.

Testing the skill itself (`/notes-api-smoke`, automatic invocation, the
exercises) needs Claude Code: copy the files into your workspace, start
`claude` in the workspace root and follow the chapter.
