# Iteration notes: ch02

Sample notes. Your code changes and results will differ, especially for
Change 2, which depends on the libraries Claude chooses.

## Change 1: add status values and a --status filter
Prompt change: added the constraint `- Task status is exactly "open" or "done".`
at the end of CONSTRAINTS, and the example
`- task list --status open -> lists only open tasks` at the end of EXAMPLES.
Code change: task.py only. The list subcommand gained a `--status` option
with choices `open` and `done`, cmd_list filters on it, and the module
docstring shows the new option. New tasks were already created as "open",
so nothing else changed.
Result: `python3 task.py list --status open` listed only task #2.
`python3 task.py list --status pending` printed the usage message and
"invalid choice: 'pending'" on stderr, and exited with 1.

## Change 2: remove "standard library only"
Prompt change: `- Language: Python 3.11, standard library only.` became
`- Language: Python 3.11.` (in a copy of the prompt in ~/cc-scratch/ch02-deps).
Code change: a fresh implementation in the scratch folder, thrown away afterwards.
Result: ran `grep -nE '^(import|from) ' *.py` and `ls`. Record here which
third-party imports appeared (for example, a library for argument parsing
or for printing tables) and whether Claude added a requirements file.
Lesson: without the constraint, every user of the tool has to install
those packages first. The constraint stays in prompt.md.
