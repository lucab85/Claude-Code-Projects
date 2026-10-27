---
name: code-review
description: Review an AI-generated diff as if it were a stranger's pull request. Output a ranked, severity-tagged list of bugs and the smallest patch per item.
---

## Purpose

Catch the bugs Claude tends to make in its own code: boundaries, error paths, hidden type assumptions, swallowed exceptions, surprise globals, and silent fallbacks.

## When to use

- After Claude produces or modifies any non-trivial code path.
- Before you commit AI-generated code.
- During Best-of-N scoring as the "Correctness" check.

Skip when: the diff is < 5 lines and entirely cosmetic.

## Body

1. Reframe Claude's role: *"You are reviewing a stranger's pull request, not your own work."* This single sentence reduces sycophancy.
2. Provide the diff (not the prompt that produced it).
3. Ask Claude to enumerate **every** potential bug across categories:
   - Off-by-one and boundary conditions.
   - Null / undefined / empty-collection handling.
   - Error paths (try/except, swallowed exceptions, unchecked returns).
   - Type coercion (especially across language boundaries: form, query, JSON).
   - Race conditions in shared state.
   - Hidden assumptions about the environment (timezone, locale, file paths).
4. Rank by severity: **Critical / High / Medium / Low**.
5. For each, ask for the **smallest** possible patch — not a rewrite.
6. Do not let Claude write code yet. Just the list.

## Inputs

- A unified diff (`git diff` output) or a code block being reviewed.
- The language and runtime version (Claude can guess, but be explicit).

## Outputs

A markdown list, one item per finding:

```text
- [Severity] One-sentence description.
  Smallest patch: <≤ 2-line fix sketch>.
```

Ordered by severity descending. Stop after 10 items per review pass.

## Worked example

Input diff (Python, FastAPI route):

```python
@app.get("/notes")
def list_notes(q: str = ""):
    rows = cx.execute(
        "SELECT * FROM notes WHERE title LIKE ? AND body LIKE ?",
        (f"%{q}%", f"%{q}%"),
    ).fetchall()
    return rows
```

Expected output:

```text
- [High] Search uses AND across title and body — a substring matching only one field returns nothing.
  Smallest patch: change `AND` to `OR` in the SQL clause.
- [Medium] Empty `q` filters via `LIKE '%%'` which matches everything but the SQL still scans;
  also returns all rows even when caller may have intended "no filter".
  Smallest patch: branch on `if q:` and run a different query when empty.
- [Low] No row limit. A pathological table size will OOM the server.
  Smallest patch: append `LIMIT 1000` and add a `?limit=` query parameter.
```
