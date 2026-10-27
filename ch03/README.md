# Chapter 3: Giving Claude Project Context with CLAUDE.md

In this chapter you write a CLAUDE.md for the `claude-code-projects`
workspace: five sections (Stack, Conventions, Commands, Do-not, Glossary),
under 80 lines. You then prove it works with a fresh-session test and a
trim test, and turn a past mistake into a new rule. The Python files here
are what Claude produced from prompts that never mentioned the conventions.

## Files

| File | What it is | Section |
|------|------------|---------|
| `CLAUDE.md` | The reviewed project brain file, including the exit-code rule added at the end of the chapter (33 lines). Copy it to the root of your workspace, not into `ch03/`. | Reviewing and trimming to 80 lines; Turning a mistake into a rule |
| `greet.py` | Greeting CLI with a `hello <name>` subcommand and an `--upper` flag, produced in the workshop with a similar CLAUDE.md in place | The fresh-session test |
| `trim-notes.md` | Example notes for the trim test, with one line you could delete and why | The trim test |
| `count.py` | Word-count CLI with a `words <file>` subcommand; every usage error exits with 1 | Turning a mistake into a rule |

## Run and test

Python 3.11 or later, standard library only. From the root of the workspace:

```bash
wc -l CLAUDE.md
grep -n '^# ' CLAUDE.md

python3 ch03/greet.py hello Students           # Hello, Students!
python3 ch03/greet.py hello Students --upper   # HELLO, STUDENTS!

python3 ch03/count.py; echo "exit code: $?"                         # 1
python3 ch03/count.py words; echo "exit code: $?"                   # 1
python3 ch03/count.py words no-such-file.txt; echo "exit code: $?"  # 1
python3 ch03/count.py words ch03/README.md                          # word count, exit 0
```

`greet.py` is kept as Claude wrote it, including the two flaws the chapter
points out: `main()` has no docstring, and `greet.py hello` without a name
exits with 2.
