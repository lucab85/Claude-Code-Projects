# Audit of the workshop's 12-item readiness report

Source: `exercises/part-10/solution/README.md` in the workshop repository.
Checked against the Notes API in ch05, as it stands at the end of
Chapter 10 (before any Chapter 11 changes). Run the commands from the
workspace root.

| # | Item and claim | Verdict | What decides it |
|---|---|---|---|
| 1 | Secrets hygiene ✓: `.env` ignored; no keys in history | VERIFIED | `grep -n "^.env$" .gitignore` matches; `git log -p \| grep -ciE "api[_-]?key\|secret\|password\|token"` prints 0 |
| 2 | AuthN/AuthZ ✗: "No auth on `/tasks` endpoints" | FALSE | The routes are `/notes`, not `/tasks` (`grep -n "@app" ch05/notes_api.py`). The finding itself, no authentication, is true. |
| 3 | Input validation ✓: Pydantic rejects an empty title | VERIFIED, but the ✓ is wrong | `test_blank_title_is_422` passes. `python3 ch11/probe.py` shows a 100,000-character title and a 5 MB body accepted with 201, so the item isn't green. |
| 4 | Error budgets ✗: no SLO for `/tasks` | FALSE | No SLO exists, but for `/notes`; there is no `/tasks` route. |
| 5 | Idempotency △: `POST /tasks` not idempotent | FALSE | Wrong route again. The substance holds for `POST /notes`: posting the same body twice creates two notes. |
| 6 | Observability ✗: no structured logs, no traces | VERIFIED | `grep -n "logging" ch05/notes_api.py` has no matches |
| 7 | Performance ✓: "p95 < 50ms on 1k tasks (smoke)" | UNCHECKABLE | No measurement exists in the workspace or the workshop materials; the smoke test checks status codes, not latency. A ✓ needs a command that proves it. |
| 8 | Backwards compatibility n/a: first release | VERIFIED | `git tag` is empty: nothing has been released |
| 9 | Disaster recovery △: SQLite file, no backup | VERIFIED | `ls ch05` shows `notes.db` and no backup or backup script |
| 10 | Rollback ✓: "Container image tagged per commit" | FALSE | `ls ch05` shows no Dockerfile or container config, and `git tag` is empty |
| 11 | Permission scope ✓: "Container runs as non-root UID 1000" | FALSE | There is no container, so nothing runs as UID 1000 |
| 12 | Human review ✓: "counter-signed by senior eng." | UNCHECKABLE | No reviewer is named and there is no signature or approval to look at |

Result: 5 VERIFIED (one of them with a wrong status), 5 FALSE,
2 UNCHECKABLE. Only one of the report's six ✓ items (secrets) holds up.
The verdict, NO-GO, is right, but two of its three blockers name a
`/tasks` route that doesn't exist, and it doesn't count the lack of input limits.

Lesson: the report is well formatted and mostly plausible, which is what
makes it dangerous. Each claim needs a command that proves it.
