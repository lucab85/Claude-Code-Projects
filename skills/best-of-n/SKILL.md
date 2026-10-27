---
name: best-of-n
description: Generate N independent candidate implementations of the same task and select the winner using a 3-criterion rubric (correctness, simplicity, fit).
---

## Purpose

Convert variance in model output into measurably better artefacts. Produce N candidates, score each on a fixed rubric, and ship the winner with explicit justification.

## When to use

- For any task where "looks right" is not enough — APIs, parsers, algorithms, schemas.
- When you have ~5 minutes to spare per N: 3 candidates ≈ 2× the wait, often >2× the quality.
- During design review: candidates make tradeoffs explicit.

Skip when: the task has one obvious correct answer (formatting, lint fixes, trivial config).

## Body

1. Author the task prompt **once**, with full GCOE structure (Goal · Constraints · Output · Examples).
2. Open **N independent chats**. Same prompt in each. N=3 is the sweet spot.
3. Save each candidate to a separate folder so they cannot influence each other.
4. Apply the rubric:
   - **Correctness (0–3)**: passes the manual test plan?
   - **Simplicity (0–3)**: would a junior engineer maintain this on day one?
   - **Fit (0–3)**: matches `CLAUDE.md` conventions and existing repo style?
5. Sum scores. Tie-breaker: simpler source wins.
6. Commit only the winner. Archive the losers in a single folder; do not delete (they are evidence of the lift).

## Inputs

- A complete GCOE task prompt.
- N (default 3).
- A short manual test plan or curl script to evaluate "Correctness".

## Outputs

```text
candidate-a/  ...source...
candidate-b/  ...source...
candidate-c/  ...source...
scoring.md    rubric scores + per-candidate one-paragraph justification
winner/       exact copy of the chosen candidate
```

`scoring.md` shape:

```text
Candidate: a
Correctness: 3/3
Simplicity:  2/3
Fit:         2/3
Total: 7/9
Notes: <one paragraph>
```

## Worked example

Task: "Build a small Notes API persisting to SQLite" (full GCOE in the originating prompt).

Three independent runs produce: (a) FastAPI single-file with everything inline; (b) FastAPI split into router + service + repo; (c) FastAPI single-file with elegant generic CRUD helper.

Scoring sample:

- A: 3 / 2 / 3 = 8 — pragmatic, matches conventions.
- B: 3 / 1 / 1 = 5 — over-architected for scope.
- C: 3 / 3 / 1 = 7 — beautiful but the helper diverges from `CLAUDE.md`.

Winner: A. Justification: max score, lowest carrying cost, on-convention.
