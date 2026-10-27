---
name: documentation-generation
description: Produce HANDOFF.md and ARCHITECTURE.md from a diff and the resulting source. Output is two short, audience-specific docs.
---

## Purpose

Turn a fresh diff into the two docs every project actually needs: a one-page handoff for the next engineer, and a one-page architecture sketch for anyone landing in the module cold.

## When to use

- Right after a refactor or a non-trivial feature merge.
- Before handing a module to a new owner.
- When onboarding pain reports the same questions twice.

Skip when: the change is < 10 lines or behavior-only.

## Body

Two passes, **never combined**.

**Pass 1 — `HANDOFF.md`** from the diff:

- Sections, in order: What changed (≤ 3 bullets) · Why · Risk + how to roll back · Watch-outs for the next engineer (specific, not generic).
- Cap at 40 lines.

**Pass 2 — `ARCHITECTURE.md`** from the resulting source (not the diff):

- One ASCII diagram (boxes + arrows) of components and data flow.
- One short paragraph per component (purpose, inputs, outputs).
- A "Known limitations" list with at most 5 items.
- Cap at 80 lines.

Reject any output that combines the two — `HANDOFF.md` describes change, `ARCHITECTURE.md` describes shape; combining them produces sludge.

## Inputs

- For pass 1: a unified diff.
- For pass 2: read access to the resulting source files.

## Outputs

Two files at the path the caller specifies (typically the module root):

```text
HANDOFF.md       ≤ 40 lines, four sections
ARCHITECTURE.md  ≤ 80 lines, diagram + components + limitations
```

## Worked example

Input: a refactor diff on `pricing.py` (7-deep nesting → early returns + module-level dicts).

`HANDOFF.md` excerpt:

```markdown
## What changed
- Replaced 7-deep nesting with early returns in `calc`.
- Extracted `_TAX_RATES` and `_SHIPPING_LADDER` to module scope.
- Removed unreachable `pass` branches.

## Why
Original was correct but unreviewable. Behavior preserved (existing tests still green).

## Risk + rollback
Low. No public signature changed. `git revert` to roll back.

## Watch-outs
- Default tax rate is 10% for unknown countries — check before adding stricter behavior.
- Coupons are case-sensitive: `'save10'` ≠ `'SAVE10'`.
```

`ARCHITECTURE.md` excerpt: ASCII diagram of items → discount selector → subtotal → tax / shipping → final, plus a paragraph per component and ≤ 5 limitations.
