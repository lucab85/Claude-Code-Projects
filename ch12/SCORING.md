# Scoring the reference solution

Scored against Table 12.5, strictly. The pass mark is 28 out of 40.

| Criterion | Points | Score | Evidence |
|---|---|---|---|
| Service runs and passes smoke.sh | 8 | 8 | `uvicorn bookmarks_api:app --port 8000` from `service/`; all seven smoke lines pass on a fresh database. |
| Tests | 6 | 6 | 8 tests, all green: 4 happy path, 3 error, 1 boundary (200-character title accepted, 201 rejected). They import the real module; no mocks. |
| PROMPT.md in GCOE form | 6 | 6 | Goal, constraints, output format and examples; every open question from step 1 is decided (see DECISIONS.md). Commit it before the service so the history shows the order. |
| candidates.md | 4 | 3 | Two candidates, scored on the three criteria, with a justified pick. One point off: candidate A got 3 for correctness, but the extra checks never tried a URL without a host, and review found exactly that bug. |
| REVIEW.md and an applied fix | 6 | 6 | Five ranked findings; two fixed, each with a test that failed before the fix. |
| PR.md | 4 | 4 | 36 lines; what, why, testing, risks, rollback and a 4-item checklist; claims checked against the files. |
| READINESS.md | 2 | 2 | Five axes with an evidence table; a 21-word No-Go verdict. |
| Clean repository | 4 | 4 | Runs from a fresh copy of `ch12/`; `.gitignore` keeps `bookmarks.db` out; service/README.md has the run and test commands. |
| Penalties | | 0 | GCOE prompt present, two candidates, no mocks, the PR says why. |
| **Total** | **40** | **39** | 97.5%, a pass. |

A 39 isn't a reason to relax. The lost point is the useful part: the
decision checks you run while scoring candidates should cover every
constraint in PROMPT.md, not just the ones that are easy to curl.

## The reflection

There is no reference reflection.md: its four sections are about bugs,
rubric items and habits from your own projects, so a sample would only
be something to copy. Score yours out of 20 as the chapter describes:
6 for two real bugs with symptom, cause, fix and what caught each; 5 for
the rubric section naming real items; 4 for a named skill with a
concrete use; 3 for a specific answer on constraints; 2 for four
sections and 400 to 700 words.
