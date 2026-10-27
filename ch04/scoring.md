# Best-of-N scoring: Notes API

Two candidates generated from the identical prompt.md in two separate
sessions, then run through the same smoke.sh.

## Smoke-test results

| Check         | Spec wants              | Candidate A          | Candidate B          |
|---------------|-------------------------|----------------------|----------------------|
| create note   | 201                     | 201 PASS             | 201 PASS             |
| blank title   | 422                     | 422 PASS             | 201 FAIL             |
| list notes    | 200                     | 200 PASS             | 200 PASS             |
| search notes  | 200                     | 200 PASS             | 200 PASS             |
| get note 1    | 200                     | 200 PASS             | 200 PASS             |
| update note 1 | 200                     | 200 PASS             | 405 FAIL (PUT, not PATCH) |
| delete note 1 | 204                     | 204 PASS             | 204 PASS             |
| missing note  | 404                     | 404 PASS             | 404 PASS             |
| 404 body      | `{"error":"not found"}` | `{"detail":{...}}`   | `{"detail":{...}}`   |

## Per-candidate scores

```text
Candidate: a
Correctness (0-3): 3  every status code matches the spec
Simplicity  (0-3): 3  one readable file
Fit         (0-3): 2  the 404 body is wrapped in detail
Total: 8 / 9
Notes: Lifespan startup hook, partial PATCH, blank title returns 422.
       Only miss is {"detail":{"error":"not found"}} instead of
       {"error":"not found"}.
```

```text
Candidate: b
Correctness (0-3): 1  PATCH returns 405, and a blank title returns 201
Simplicity  (0-3): 2  clean, but repeats the same row-to-note conversion
                      in every route
Fit         (0-3): 1  wrong update method, no validation, wrapped 404 and
                      a deprecated startup hook (@app.on_event)
Total: 4 / 9
Notes: Implemented PUT instead of PATCH and skipped input validation.
```

## Side by side

| Criterion (0-3) | Candidate A | Candidate B |
|-----------------|-------------|-------------|
| Correctness     | 3: every status code matches the spec | 1: PATCH returns 405, and a blank title returns 201 |
| Simplicity      | 3: one readable file | 2: clean, but repeats the same row-to-note conversion in every route |
| Fit             | 2: the 404 body is wrapped in detail | 1: wrong update method, no validation, wrapped 404 and a deprecated startup hook |
| Total           | 8 / 9 | 4 / 9 |

## Decision

Winner: Candidate A (8/9 vs 4/9). A passes every smoke check; B fails two
spec requirements outright (PATCH returns 405 because it implemented PUT,
and a blank title is accepted with 201 instead of 422). Both share the
wrapped 404 body, so that doesn't separate them. B is kept as evidence.
