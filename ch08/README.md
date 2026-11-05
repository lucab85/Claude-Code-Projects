# Chapter 8: Constrained Refactoring and Documentation from the Diff

Project 8 refactors a deliberately messy pricing module under written constraints, pins its behavior with a golden master first, and then writes `HANDOFF.md` and `ARCHITECTURE.md` from the diff.

| Folder | What it holds | Section |
| --- | --- | --- |
| `start/` | The legacy `pricing.py` and its 8 passing tests. The mess is intentional | Setting up and reading the legacy code |
| `workshop-refactor/` | An earlier refactor, with its `HANDOFF.md` and `ARCHITECTURE.md`. It passes all 8 tests but changes behavior, and its documents don't match its code | Testing the safety net on a real refactor; Exercise 8.2 |
| `solution/` | The finished project: refactored `pricing.py`, `golden.py`, `golden.json` recorded from the legacy code, `constraints.md`, `HANDOFF.md` and `ARCHITECTURE.md` | Project 8 |

Check the reference solution from its folder:

```bash
cd ch08/solution
python3 -m pytest -q          # 8 passed
python3 golden.py check       # 576 same, 0 changed
```

Run the same two commands in `workshop-refactor/` after copying `golden.py` and `golden.json` there, and the golden master reports 162 changed cases.

The mismatches between `workshop-refactor/pricing.py` and its two documents are deliberate. Don't fix them; they are the answer key for Exercise 8.2.
