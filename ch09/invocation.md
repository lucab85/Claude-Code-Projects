# notes-api-smoke: recorded run

Date: 2026-10-27

Command, run from the workspace root with the virtual environment active.
This is the command that `/notes-api-smoke ch05/notes_api.py` runs:

    python3 .claude/skills/notes-api-smoke/smoke.py ch05/notes_api.py

Output, unedited:

    PASS  create note (201)
    PASS  blank title rejected (422)
    PASS  list notes (200)
    PASS  search notes (200)
    PASS  get note (200)
    PASS  update note (200)
    PASS  delete note (204)
    PASS  deleted note is 404 (404 {"error": "not found"})
    RESULT: PASS

Exit code: 0
