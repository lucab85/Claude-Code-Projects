GOAL
Build a single-file CLI Task Manager so a developer can manage TODOs
from the terminal.

CONSTRAINTS
- Language: Python 3.11, standard library only.
- Persistence: a single JSON file, tasks.json, in the current directory.
- No background processes. No network calls.
- Exit code 0 on success, 1 on user error, 2 on internal error.
- All user-facing strings in English.
- Task status is exactly "open" or "done".

OUTPUT FORMAT
- One source file, task.py.
- A short README.md explaining the four commands.

EXAMPLES
- task add "Write the spec" -> prints "Added task #1: Write the spec"
- task list -> table with columns: id, status, created_at, text
- task done 1 -> prints "Marked #1 as done"
- task delete 99 -> exit 1, prints "No task with id 99"
- task list --status open -> lists only open tasks
