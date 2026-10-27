# Chapter 11 practice exercises

Files for the six exercises at the end of Chapter 11. Do them on a
practice branch, such as `practice/ch11`, and run every command from the
workspace root. The chapter has the goals, checks and hints; this page
only says how each file fits in.

## 11.1 Audit a readiness report

`11.1-audit/audit.md` is a reference answer: each of the workshop's 12
claims marked VERIFIED, FALSE or UNCHECKABLE, with the command or file
that decides it. Write your own ch11/audit.md first.

## 11.2 Catch an injection with /security-review

1. In `list_notes()` in ch05/notes_api.py, replace the whole
   parameterized `rows = conn.execute(...).fetchall()` call inside
   `if q:` with the four lines in `11.2-sql-injection/planted-query.txt`,
   indented to match.
2. `python3 -m pytest -q ch05/tests`: one test fails,
   `test_search_treats_wildcards_literally`.
3. `python3 ch11/exercises/11.2-sql-injection/probe_injection.py`
   creates a "public" and a "private" note on a scratch database and
   searches for `zzz' OR 1=1 --`. With the planted query it prints both
   titles and `INJECTION`; after `git revert HEAD` it prints `[]` and
   `SAFE: no note contains zzz`.

## 11.3 Add input limits

`11.3-input-limits/input-limits.diff` is the change from the chapter (an
excerpt; `...` marks unchanged lines, and `Field` must be imported from
pydantic). `tests-to-add.py` has one test for each limit; add them
first and watch them fail. Afterwards: 16 tests pass and the probe's
first line reads `100,000-char title + 5 MB body: 422`.

## 11.4 Write a runbook and test it

`11.4-runbook/RUNBOOK.md` is a reference ch05/RUNBOOK.md: five failures,
each with a symptom, a first command and when to escalate. Try every
command on your own machine before you trust it.

## 11.5 Run a rollback drill

`11.5-rollback-drill/drill.md` lists the drill's commands in order.

## 11.6 Pin the deployment

`11.6-pin-deployment/requirements.txt` is the reference freeze: the 14
runtime packages, including fastapi==0.143.0, pydantic==2.14.0,
starlette==1.7.0 and uvicorn==0.54.0. Build your own in a clean
environment as the chapter shows, then compare. `requirements-dev.txt`
adds the test tools on top; copy both into ch05. A Production section
for ch05/README.md can be as short as this:

```markdown
## Production

Install and run from ch05:

    python3 -m venv .venv
    .venv/bin/pip install -r requirements.txt
    .venv/bin/python -m uvicorn notes_api:app --host 127.0.0.1 --port 8000

No --reload in production. The API has no authentication yet, so keep it
on 127.0.0.1 and put a reverse proxy in front if other machines need it.
```
