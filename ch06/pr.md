## Summary
Fixes two bugs found while reviewing the Notes API and adds a test
suite covering every endpoint. Also lets Claude Code run the tests
without asking and blocks it from reading .env files.

## Why
A stranger's-PR review of the Chapter 4 winner found that search treated
% and _ as wildcards and that every request leaked a SQLite connection.
Neither showed up in the smoke test.

## What changed
- notes_api.py: get_db() now always closes its connection.
- notes_api.py: search escapes LIKE wildcards (new _like_pattern helper).
- tests/test_notes_api.py: 13 pytest tests, including a regression test
  for wildcard search and exact 404 bodies.
- ch05: bug-fix notes and a code review rubric.
- .claude/settings.json: allow `python3 -m pytest`, deny reading .env.

## How to test
    source ch04/.venv/bin/activate
    python3 -m pytest -q -W default::ResourceWarning ch05/tests

## Risk
Low. The API contract is unchanged. get_db() now closes connections, so
code that kept using a connection after its `with` block would break;
no code does.

## Rollback
Revert the merge commit. There are no data migrations.

## Reviewer checklist
- [ ] Do all 13 tests pass with no ResourceWarning?
- [ ] Does GET /notes?q=% return only notes that contain "%"?
- [ ] Is every get_db() call used inside a `with` block?
- [ ] Is .env listed in .gitignore?
