# HANDOFF — pricing.py refactor (reference)

## What changed

- Replaced 7-deep nesting with early-return guards in `calc`.
- Extracted tax and shipping rate lookups into module-level dicts.
- Removed unreachable `pass` branches.

## Why

The original was correct but unreviewable. Every change preserves byte-identical behavior (the existing test suite still passes) while shrinking the function from 50 lines to ~20.

## Risk + rollback

Risk: low. No public signature changed; no new dependencies. To roll back: `git revert` the refactor commit.

## Watch-outs for the next engineer

- The default tax rate is **10%** for unknown countries. If product asks for a stricter behavior, change `_TAX_RATES.get(country, 0.10)` and add a test.
- Coupon codes are matched exactly (case-sensitive). `'save10'` ≠ `'SAVE10'`.
- The free-shipping threshold of 200 is duplicated in test code — if business changes this, update both.
