# Chapter 12: Capstone reference solution

> **Spoiler warning.** This folder is the reference solution for the
> Bookmarks API capstone. Don't open the files until you've finished
> your own capstone, scored it and written your reflection. Then compare
> decisions, not lines.

Chapter 12 condenses the book into three frameworks (the loop, the
scoring rubric and the readiness review) and ends with a capstone: a
Bookmarks API built from a two-line brief, with the artifacts that show
how you got there. This folder holds one complete answer: the service,
its tests, the smoke test and every document the capstone asks for.

## Files

| File | What it is | Section |
|---|---|---|
| `CLAUDE.md` | Folder rules: the stack, layout and commands for ch12 | Step 1: Set up and plan |
| `PROMPT.md` | The GCOE prompt, with the open questions decided | Step 1: Set up and plan |
| `DECISIONS.md` | Each open question in the brief, the reference choice and why | Step 1: Set up and plan |
| `candidates.md` | Two candidates scored 0 to 3 on correctness, simplicity and fit, and the pick | Step 2: Generate two candidates |
| `smoke.sh` | The contract as curl commands, exactly as listed in the chapter | Step 3: Write the smoke test |
| `service/bookmarks_api.py` | The service: FastAPI and SQLite in one file | Steps 2 to 5 |
| `service/tests/test_bookmarks_api.py` | 8 tests: 4 happy path, 3 error, 1 boundary | Step 4: Generate the tests |
| `service/README.md` | Run and test commands, and the endpoints | Step 7: Ship it |
| `REVIEW.md` | Ranked review findings, the two fixes and their tests | Step 5: Review and fix |
| `READINESS.md` | Five axes, evidence and a No-Go verdict | Step 6: Assess readiness |
| `PR.md` | The pull request description, 36 lines | Step 7: Ship it |
| `SCORING.md` | The reference scored against the capstone rubric | Scoring your capstone |
| `.gitignore` | Keeps `bookmarks.db` and `__pycache__` out of Git | Clean repository |

There is no reference `reflection.md` (step 8): it's about your own
work across the book. SCORING.md explains how to score yours.

## Run and test

You need Python 3.11 or later with `fastapi`, `uvicorn`, `pytest` and
`httpx2` (or `httpx`), for example the virtual environment from
Chapter 4.

```bash
# Tests, from the repository root
python3 -m pytest -q ch12/service/tests
# ........                                                     [100%]
# 8 passed in 0.38s

# Smoke test: start the service on a fresh database...
cd ch12/service
rm -f bookmarks.db
uvicorn bookmarks_api:app --port 8000

# ...then, in a second terminal, from the repository root
ch12/smoke.sh 8000
# PASS  create (201) ... RESULT: PASS
```

smoke.sh fetches bookmark 1, so delete `bookmarks.db` before each run.
