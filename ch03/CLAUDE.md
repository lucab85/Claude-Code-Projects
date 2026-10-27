# Stack
- Python 3.11+, standard library only at runtime.
- Data files are JSON, indented with 2 spaces.
- One folder per chapter project: ch01/, ch02/, ch03/ and so on.

# Conventions
Python files:
- Start executable scripts with `#!/usr/bin/env python3`.
- Use one-line docstrings, such as `"""Load tasks."""`.
- Parse arguments with `argparse` and subcommands (not Click or Fire).
- Exit codes: 0 success, 1 user error, 2 internal error.
- Timestamps: ISO 8601 in UTC, `datetime.now(timezone.utc).isoformat()`.
- Print errors to stderr, never to stdout.

Layout:
- Keep each chapter project self-contained inside its chNN/ folder.
- Every project has a README.md with usage for each command.

# Commands
- Run a CLI:  python3 ch02/task.py list
- Run tests:  python3 -m pytest -q
- Lint:       ruff check .

# Do-not
- Never add runtime dependencies; dev tools (pytest, ruff) are fine.
- Never commit generated data such as tasks.json; it is in .gitignore.
- Never edit another chapter's folder unless asked.
- Never swallow exceptions; surface them with the exit codes above.
- Never let argparse exit with 2 on usage errors; user errors exit with 1.

# Glossary
- Chapter project: the deliverable in a chNN/ folder.
- GCOE: Goal, Constraints, Output, Examples; see ch02/prompt.md.
