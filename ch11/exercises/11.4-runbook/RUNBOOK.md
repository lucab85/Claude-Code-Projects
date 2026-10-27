# Notes API runbook

Run every command from the workspace root. The API runs from ch05 with
`python3 -m uvicorn notes_api:app --host 127.0.0.1 --port 8000`.

## 1. Health check failing
- Symptom: `GET /health` returns 500 or nothing at all.
- First action: `curl -s -w ' %{http_code}\n' http://127.0.0.1:8000/health`.
  `000` means nothing is listening: check the process with
  `pgrep -fl "uvicorn notes_api"` and restart it. A 500 means the API
  is up but can't use the database: go to entry 2.
- Escalate: if it still fails five minutes after a restart.

## 2. "database is locked" errors
- Symptom: 500s, and `sqlite3.OperationalError: database is locked` in
  the server log.
- First action: find what holds the file with `lsof ch05/notes.db*`,
  then check the database:
  `python3 -c "import sqlite3; print(sqlite3.connect('ch05/notes.db').execute('PRAGMA integrity_check').fetchone())"`.
  `('ok',)` means it's healthy; stop the other process and retry.
- Escalate: if the check prints anything other than `('ok',)`. Don't
  write to the file; restore the last backup (entry 5).

## 3. Port already in use
- Symptom: uvicorn exits with `[Errno 48] ... address already in use`
  (`[Errno 98]` on Linux).
- First action: `lsof -nP -iTCP:8000 -sTCP:LISTEN` shows the process.
  If it's an old copy of the API, stop it with `kill <PID>`.
- Escalate: if it's another service; don't kill what you don't own.

## 4. Disk full
- Symptom: writes fail with `database or disk is full`.
- First action: `df -h ch05` for free space, then
  `du -sh ch05/notes.db*` for the database's share.
- Escalate: before deleting anything. Notes are user data.

## 5. Bad release
- Symptom: the smoke test fails, or users report errors, after a deploy.
- First action: stop the API, then
  `git revert --no-edit HEAD` and
  `python3 .claude/skills/notes-api-smoke/smoke.py ch05/notes_api.py`.
  If data was damaged, restore the backup taken before the deploy:
  `cp ch05/notes.db.v1.0.0 ch05/notes.db`. Start the API again.
- Escalate: if the revert conflicts or the smoke test still fails.
  The full drill is in Exercise 11.5.
