# Refactor constraints: ch08/pricing.py

## Goal
Make calc() easy to read and change. Readability only.

## Must not change
- The public signature: calc(items, country, customer).
- Behavior for any input. Both checks must pass:
  - python3 -m pytest -q          -> 8 passed
  - python3 golden.py check       -> 0 changed
- Files: edit pricing.py only. No new files, dependencies or imports.
- Never edit test_pricing.py, golden.py or golden.json.

## May change
- Local variable names, when the new name is clearly better.
- Nested ifs into guard clauses (continue or early return).
- Small private helpers inside pricing.py, named with a leading _.
- Fixed data, such as tax rates, moved into module-level tables.

## Must not do
- "While I'm here" fixes. If you spot a bug, list it; don't fix it.
- Comments, except to explain a non-obvious why.
- Catching exceptions that the current code lets through.
