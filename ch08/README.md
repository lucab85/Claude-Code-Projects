# Chapter 8: Constrained Refactoring and Documentation from the Diff

Project 8 refactors a deliberately messy pricing module under written constraints, pins its behavior with a golden master first, and then writes `HANDOFF.md` and `ARCHITECTURE.md` from the diff.

| File | What it is |
|---|---|
| `legacy/pricing.py` | The legacy module you refactor. The mess is intentional. |
| `legacy/test_pricing.py` | Its existing tests (8, all passing). Passing them isn't enough to prove a refactor is safe; that's the point of the golden master. |

```bash
cd ch08/legacy
python3 -m pytest -q
```

The golden-master script, `constraints.md` and the reference docs will be added here when the chapter is final.
