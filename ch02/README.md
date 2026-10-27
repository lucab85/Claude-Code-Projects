# Chapter 2: Prompting Like a Tech Lead with GCOE

Project 2 builds a command-line task manager from a single GCOE prompt (Goal,
Constraints, Output, Examples). The tool is one Python file that uses only the
standard library and stores tasks in `tasks.json` in the current directory.
This folder holds the prompt and the reference solution as they stand at the
end of the chapter: the `--status` filter from *Adding status filters* is in
place, and usage errors exit with 1 after the fix in *Reviewing the generated
code*.

| File | What it is | Used in |
|---|---|---|
| `prompt.md` | The GCOE prompt, including the status constraint and example from Change 1 | Writing the prompt; Adding status filters |
| `task.py` | Reference task manager, Python 3.11+, standard library only | Generating the code; Validating add, list, done and delete; Testing exit codes; Reviewing the generated code |
| `README.md` | This file, including usage for the four commands | Generating the code |
| `iteration-notes.md` | Sample notes for the two prompt changes | Iterating one constraint at a time |

## Usage

Run the commands from this folder. Tasks are saved to `tasks.json` in the
current directory and survive between runs.

```bash
python3 task.py add "Write the spec"     # Added task #1: Write the spec
python3 task.py list                     # table: id, status, created_at, text
python3 task.py list --status open       # only open tasks (open or done)
python3 task.py done 1                   # Marked #1 as done
python3 task.py delete 1                 # Deleted #1
```

Exit codes: `0` on success, `1` on a user error (unknown ID, empty text, bad
command or argument), `2` on an internal error such as a corrupt `tasks.json`,
which is never overwritten. Error messages go to stderr.

## Testing

Run the chapter's test plan (Table 2.3) from this folder:

```bash
rm -f tasks.json
python3 task.py add "Write the spec"
python3 task.py add "Review the PR"
python3 task.py done 1
python3 task.py list
python3 task.py delete 99; echo "exit code: $?"        # 1
python3 task.py add ""; echo "exit code: $?"           # 1
python3 task.py frobnicate; echo "exit code: $?"       # 1
python3 task.py done abc; echo "exit code: $?"         # 1
python3 task.py list --status pending; echo "exit code: $?"  # 1
cp tasks.json tasks.json.bak
echo 'not json' > tasks.json
python3 task.py add "Test"; echo "exit code: $?"       # 2
cat tasks.json                                         # still: not json
mv tasks.json.bak tasks.json
rm tasks.json
```

On Python 3.12, argparse prints the allowed choices without quotes, for
example `(choose from open, done)`. The exit codes are the same on every
supported version.
