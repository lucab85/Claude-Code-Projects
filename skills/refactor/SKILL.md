---
name: refactor
description: Refactor a module under hard written constraints. Output a unified diff that respects every constraint and preserves byte-identical behavior.
---

## Purpose

Make AI refactors shippable. Constraints are what stop a "tidy-up" from becoming a rewrite. The output is a diff you can read in one sitting.

## When to use

- A module is correct but unreviewable.
- The existing test suite is green and you want to keep it that way.
- You need readability gains without behavioral risk.

Skip when: the right move is a redesign (different boundaries, new dependencies, schema change). Refactors do not redesign.

## Body

1. Write `constraints.md` **before** prompting. Constraints fall into three groups:
   - **Lock-in**: what may not change (public signatures, file count, deps, behavior).
   - **Permitted moves**: what is welcomed (early returns, rename locals, extract pure helpers in same file).
   - **Forbidden moves**: comments-as-explanations, "while you're at it" changes, broadening exception types.
2. Prompt Claude with the full source and the constraint list. Ask for **a unified diff only** — no prose.
3. Apply the diff. Re-run the existing test suite. Must remain green.
4. If a constraint was violated, reject and re-prompt with the violation called out specifically.

## Inputs

- Source file(s) to refactor.
- An existing test suite that is currently green.
- A `constraints.md` document authored before the prompt.

## Outputs

- A unified diff applied to the source.
- A green test run of the unchanged suite.
- A short `HANDOFF.md` (often produced by the `documentation-generation` skill in a follow-up pass).

## Worked example

Input: a 50-line `pricing.py` with 7-deep nested conditionals; existing pytest suite green.

`constraints.md`:

```text
Lock-in:
- Public function signature `calc(items, country, customer)` unchanged.
- No new files. No new deps. No new imports.
- Existing tests must remain byte-identical green.
Permitted:
- Replace nested conditionals with early returns.
- Extract module-level dicts for static lookups (tax rates).
- Rename locals only when materially clearer.
Forbidden:
- Adding comments. Renaming the public function. Catching new exception types.
```

Output: a diff that drops nesting from 7 to 2 levels, factors `_TAX_RATES` and `_SHIPPING_LADDER` to module level, removes unreachable `pass` branches, and leaves the public surface untouched. Tests still pass.
