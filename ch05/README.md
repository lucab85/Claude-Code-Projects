# Chapter 5: Testing, Debugging and Self-Review of AI-Generated Code

This folder holds the Notes API from Chapter 4 after it has been tested and
reviewed. A pytest suite runs the real `notes_api.py` against a fresh SQLite
file for every test. Two bugs were planted to prove the suite works, and a
review framed as a stranger's pull request found two real bugs that every
test had missed: unescaped `LIKE` wildcards in search and database
connections that were never closed. Both are fixed here, each with a test.

## Files

| File | What it is | Section |
| --- | --- | --- |
| `notes_api.py` | The Notes API (FastAPI and SQLite), with the wildcard and connection-leak fixes | Project 5; Fixing and re-running the tests |
| `tests/test_notes_api.py` | The persistent test suite: 12 tests, plus `test_search_treats_wildcards_literally` | Writing the test prompt; Fixing and re-running the tests |
| `bug-fix-notes.md` | Symptom, cause, diagnosis and fix for the two planted and two real bugs | Planting and catching bugs; Triaging the bug list |
| `code-review-rubric.md` | Sample personal code review checklist | Building your code review rubric |
| `.claude/settings.json` | Permission rules: run `python3 -m pytest` without asking, never read `.env` | Letting Claude run your tests safely |
| `README.md` | This file | Project 5 |

The chapter puts `.claude/settings.json` at the root of the
`claude-code-projects` workspace. Copy it there; it is kept in this folder
only so that it ships with the chapter.

## API

| Method | Path | Body | Status |
| --- | --- | --- | --- |
| POST | `/notes` | `{"title":"…","body":"…"}` | 201 / 422 |
| GET | `/notes?q=` | none | 200 |
| GET | `/notes/{id}` | none | 200 / 404 |
| PATCH | `/notes/{id}` | `{"title":"…","body":"…"}` (partial) | 200 / 404 / 422 |
| DELETE | `/notes/{id}` | none | 204 / 404 |

A missing note returns `{"error": "not found"}`. Search matches the title
or the body, and `%`, `_` and `\` in `q` are matched literally.

## Run and test

Use the virtual environment from Chapter 4 (FastAPI and uvicorn are already
installed there):

```bash
source ../ch04/.venv/bin/activate
pip install pytest httpx2        # or httpx, if httpx2 isn't available
python3 -m pytest -q -W default::ResourceWarning
```

Expected result: `13 passed`, with no warnings.

To run the API and the Chapter 4 smoke test:

```bash
uvicorn notes_api:app --port 8005
../ch04/smoke.sh 8005            # in a second terminal
```

To see the suite catch bugs, run it against the Chapter 4 losing candidate
(expect `5 failed, 7 passed` on the first 12 tests), or plant the two bugs
from the chapter in `notes_api.py` before the fixes (expect `3 failed`).
