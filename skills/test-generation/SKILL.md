---
name: test-generation
description: Generate a real, runnable test suite for a given module. Covers happy path, error paths, and at least one boundary case per public function.
---

## Purpose

Produce a test suite that exercises the same code paths real callers will, with no SUT mocking and at least one boundary test per public function.

## When to use

- After Claude generates a new module and before the first commit.
- After a refactor (`HANDOFF.md` should reference the green test run).
- Whenever a module has < 80% line coverage and no behavioral tests.

Skip when: the module is a thin glue layer with zero branching.

## Body

1. Read the module's public surface (exports / route handlers / CLI commands).
2. Pick the framework appropriate to the runtime: `pytest` (Python), `vitest` (Node + TS).
3. For each public entry point, generate **at minimum**:
   - One happy-path test.
   - One error-path test (invalid input, missing resource, etc.).
   - One boundary test (empty string, zero, max id, off-by-one).
4. Use real I/O against ephemeral resources (tmpfs SQLite, in-memory HTTP via the framework's test client).
5. **Do not** mock the SUT itself — only true external dependencies (third-party APIs, system clock if asserted on).
6. Run the suite. Iterate until green on the existing implementation.

## Inputs

- The path to a module (file or folder).
- The runtime: Python 3.11+ or Node 20+.
- Optionally: a list of public functions / endpoints to prioritize.

## Outputs

- A `tests/` directory (or `test/` for Node) with one or more test files.
- All tests pass against the unmodified SUT.
- Coverage of every public entry point with the three test types above.
- A 5-line README explaining how to run.

## Worked example

Input: a FastAPI Notes API at `app.py`.

Output: `tests/test_notes_api.py` with tests for:

- `test_create_returns_201_and_body` (happy)
- `test_create_invalid_body_returns_422` (error)
- `test_search_empty_query_returns_all` (boundary)
- `test_get_one_404` (error)
- `test_delete_204_then_404` (boundary: idempotency)

Each test uses `fastapi.testclient.TestClient` against a per-test SQLite tempfile. No mocks of the route handlers or DB layer.
