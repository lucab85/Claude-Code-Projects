# Rollback drill (Exercise 11.5)

Run from the workspace root, on a practice branch, with the API stopped.
Note the time at the start and at the end.

1. Tag the good version and back up its database:

   ```bash
   git tag v1.0.0
   python3 -c "import sqlite3; (sqlite3.connect('ch05/notes.db')
     .backup(sqlite3.connect('ch05/notes.db.v1.0.0')))"
   ```

   The extra parentheses let the Python statement continue onto the
   second line. The backup's name starts with `notes.db`, so the
   `.gitignore` rule from Chapter 4 keeps it out of Git.

2. Simulate a bad release: plant the delete bug from Chapter 9 in
   ch05/notes_api.py and commit it with `git commit --no-verify`, the
   one flag that skips your Git hook.

3. Roll back and check:

   ```bash
   git revert --no-edit HEAD
   python3 .claude/skills/notes-api-smoke/smoke.py ch05/notes_api.py
   git diff v1.0.0 --stat -- ch05
   ```

4. Restore the data: `cp ch05/notes.db.v1.0.0 ch05/notes.db`.

Check: the smoke test prints RESULT: PASS, `git diff v1.0.0 -- ch05`
shows nothing, and the drill took well under 15 minutes. Copy these
steps into the bad-release entry of your runbook.
