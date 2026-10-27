# ch12: Bookmarks API (capstone)

## What
- New single-file FastAPI service, `ch12/service/bookmarks_api.py`:
  POST, GET (with an exact `?tag=` filter), GET by id and DELETE on
  `/bookmarks`, stored in SQLite.
- 8 pytest tests, `ch12/smoke.sh` for the contract, and the planning
  and review documents: PROMPT.md, DECISIONS.md, candidates.md,
  REVIEW.md, READINESS.md.

## Why
- The team asked for a small place to save and find links by tag.
- The open questions in the two-line brief (valid URLs, tag matching,
  duplicates) are decided in PROMPT.md, so reviewers can check the
  code against a written spec rather than a guess.

## How it was tested
- `python3 -m pytest -q ch12/service/tests`: 8 passed (4 happy path,
  one of them pinning the exact tag match; 3 error; 1 boundary).
- `ch12/smoke.sh 8000` on a fresh database: RESULT: PASS.
- The two review fixes each have a test that failed before the fix.

## Risks
- No authentication, logging or health check: READINESS.md is a
  No-Go for any public deployment. Run it on localhost only.
- No paging on GET /bookmarks; fine at this size.

## Rollback
- Self-contained in `ch12/`; revert the merge commit. No other code or
  shared data is touched.

## Reviewer checklist
- [ ] The tests import the real module and assert 404 bodies exactly.
- [ ] `ftp://x`, `javascript:alert(1)` and `http://` are rejected (422).
- [ ] `?tag=Misc` doesn't match `misc`, and `?tag=` returns `[]`.
- [ ] smoke.sh passes on a fresh database.
