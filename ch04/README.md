# Chapter 4: Building Faster with Best-of-N

In this chapter you generate two independent versions of a Notes API
(FastAPI, Pydantic v2 and SQLite) from the same prompt, run the same smoke
test against both, score them on correctness, simplicity and fit, and ship
the winner. The candidates here are from the reference run used in the
chapter: Candidate A wins 8/9, Candidate B scores 4/9. `winner/` is
Candidate A plus the exception handler that makes the 404 body match the
spec.

## Files

| File | What it is | Section |
|------|------------|---------|
| `CLAUDE.md` | Folder-level CLAUDE.md that allows FastAPI, Pydantic v2 and uvicorn in `ch04/` only | Setting up candidate folders |
| `prompt.md` | The GCOE prompt used for every candidate. The last EXAMPLES line (PATCH) is the one added at the end of the chapter; the reference candidates were generated before it | Setting up candidate folders; Fixing the winner's defects |
| `smoke.sh` | Eight curl checks plus the 404 body. Usage: `./smoke.sh [port]` | Smoke-testing with curl |
| `scoring.md` | Rubric scores, side-by-side table and decision | Writing scoring.md |
| `candidate-a/` | First candidate (`notes_api.py`), the winner, kept unchanged | Generating Candidate A; Comparing side by side |
| `candidate-b/` | Second candidate (`app.py`), kept as evidence: uses PUT and skips validation | Generating Candidate B in a fresh session |
| `winner/` | Copy of Candidate A with the 404-body exception handler added | Promoting the winner; Fixing the winner's defects |
| `requirements.txt` | Package versions the folder was tested with | Setting up candidate folders |
| `.gitignore` | Keeps `.venv/`, `__pycache__/` and `notes.db*` out of Git | Setting up candidate folders |

## Run and test

Use bash (the `notes.db*` glob behaves differently in zsh when nothing
matches). From `ch04/`:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Terminal 1, start a candidate (one at a time):

```bash
cd candidate-a && rm -f notes.db* && uvicorn notes_api:app --port 8001
cd candidate-b && rm -f notes.db* && uvicorn app:app --port 8002
cd winner      && rm -f notes.db* && uvicorn notes_api:app --port 8003
```

Terminal 2, from `ch04/`:

```bash
./smoke.sh 8001   # 8 PASS, 404 body {"detail":{"error":"not found"}}
./smoke.sh 8002   # FAIL blank title (201) and update note 1 (405)
./smoke.sh 8003   # 8 PASS, 404 body {"error":"not found"}
```

Tested with Python 3.11, FastAPI 0.162.0, Pydantic 2.14.1, Starlette
1.10.0 and uvicorn 0.54.0.
