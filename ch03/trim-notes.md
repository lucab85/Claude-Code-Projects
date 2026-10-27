# Trim test notes

An example of the notes you write after the trim test. Replace the
observations with what you saw in your own run.

## Setup

- Removed: the whole Conventions section of CLAUDE.md (not committed).
- Prompt: the greet.py prompt, saved as ch03/greet_trim.py, in a fresh session.
- Compared with: `diff ch03/greet.py ch03/greet_trim.py`
- Restored with: `git restore CLAUDE.md`

## What to record

| Convention          | greet.py (full CLAUDE.md) | greet_trim.py (no Conventions) |
|---------------------|---------------------------|--------------------------------|
| Shebang on line 1   | yes                       |                                |
| One-line docstrings | yes                       |                                |
| argparse subcommand | yes                       |                                |
| Exit 1 on no command | yes                      |                                |

Any row that changed is behavior the Conventions section was buying you.
If nothing changed, Claude may be copying the style of existing files
such as ch02/task.py; note that too.

## One line I could delete

- Glossary: "Chapter project: the deliverable in a chNN/ folder."
  Why: the Stack section already says there is one folder per chapter
  project, so this line doesn't change what Claude does.

## Stretch: biggest change per section

| Section removed | What changed |
|-----------------|--------------|
| Stack           |              |
| Conventions     |              |
| Commands        |              |
| Do-not          |              |
| Glossary        |              |
