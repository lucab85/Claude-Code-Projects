---
name: notes-api-smoke
description: Start a Notes API and check every endpoint, PASS or FAIL.
when_to_use: After changing a Notes API, before a commit, or to check it.
argument-hint: "[module-path] [port]"
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/smoke.py *)
---

# Notes API smoke test

## Purpose
Prove in one command that a Notes API still works end to end: it starts,
creates, lists, searches, reads, updates and deletes a note, rejects a
blank title, treats % in a search as a literal character, and returns the
agreed 404 body.

## When to use
- After any change to a Notes API module, before committing it.
- When someone asks whether the Notes API works.
- Not for unit tests: use the project's pytest suite for those.

## Body
1. Read the inputs from: $ARGUMENTS
   The first is the module path and the second, optional, is the port.
   If no path was given, find the Notes API module in the current folder
   (a .py file that defines `app = FastAPI(...)` and a /notes route) and
   ask me if there is more than one.
2. Run exactly:
   python3 ${CLAUDE_SKILL_DIR}/smoke.py <module-path> [port]
3. Show the output exactly as printed. Never edit, reorder or invent
   results, and never report PASS unless the script printed it.
4. If any line says FAIL, read the module and give the most likely cause
   of each failure, with file and line number. Don't change any code
   unless I ask.

## Inputs
- module-path: path to a single-file FastAPI app with a module-level
  `app` and the /notes routes.
- port: a free TCP port. Default 8099.

## Outputs
- One PASS or FAIL line per check, then `RESULT: PASS` or `RESULT: FAIL`.
- The script exits 0 when every check passes and 1 otherwise.
- For failures: one likely cause per FAIL, with a file and line number.

## Worked example
/notes-api-smoke ch05/notes_api.py 8099

    PASS  create note (201)
    PASS  blank title rejected (422)
    PASS  list notes (200)
    PASS  search notes (200)
    PASS  search treats % literally (200)
    PASS  get note (200)
    PASS  update note (200)
    PASS  delete note (204)
    PASS  deleted note is 404 (404 {"error": "not found"})
    RESULT: PASS
