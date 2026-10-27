# Chapter 11: Production readiness reviews

Chapter 11 reviews the Notes API from Chapter 5 on five readiness axes
(security, observability, deployment, runbooks and rollback), backs every
status with evidence and ends in a go or no-go verdict. It then takes the
smallest next step, a health endpoint, shows how to contain an agent that
does more than you asked, and introduces spec-driven development. This
folder has the probe script, the reference report and follow-up list,
and the files for the safety experiment and the six exercises.

## Files

| File | What it is | Section |
|---|---|---|
| `probe.py` | Collects evidence from the real Notes API on a scratch database | Checking each axis yourself |
| `readiness-report.md` | Reference report: five axes and a No-Go verdict | Running the review skill |
| `follow-up.md` | Reference work list built from the report, cheapest step first | Turning gaps into work |
| `health/prompt.txt` | The test-first prompt for GET /health | Taking the smallest next step |
| `health/health-route.diff` | The route Claude should add | Taking the smallest next step |
| `health/test-to-add.py` | `test_health_reports_ok`, for ch05/tests/test_notes_api.py | Taking the smallest next step |
| `safety/setup-tidy-trap.sh` | Creates the scratch folder with a fake `.env.old`, all committed | Testing the tidy-up trap yourself |
| `safety/tidy-scoped-prompt.txt` | The tidy-up prompt with the scope spelled out | Testing the tidy-up trap yourself |
| `safety/settings.json` | The cautious permissions profile for `.claude/settings.json` | A cautious permissions profile |
| `exercises/README.md` | How to use the exercise files | Practice exercises |
| `exercises/11.1-audit/audit.md` | Reference audit of the workshop's 12-item report | Exercise 11.1 |
| `exercises/11.2-sql-injection/planted-query.txt` | The f-string query to plant in `list_notes()` | Exercise 11.2 |
| `exercises/11.2-sql-injection/probe_injection.py` | Shows whether `zzz' OR 1=1 --` returns every note | Exercise 11.2 |
| `exercises/11.3-input-limits/input-limits.diff` | The input-limits change, as in the chapter | Exercise 11.3 |
| `exercises/11.3-input-limits/tests-to-add.py` | One test for each limit | Exercise 11.3 |
| `exercises/11.4-runbook/RUNBOOK.md` | Reference runbook: five failures and the first command for each | Exercise 11.4 |
| `exercises/11.5-rollback-drill/drill.md` | The rollback drill's commands, in order | Exercise 11.5 |
| `exercises/11.6-pin-deployment/requirements.txt` | Reference freeze of the 14 runtime packages | Exercise 11.6 |
| `exercises/11.6-pin-deployment/requirements-dev.txt` | The runtime packages plus pytest and httpx2 | Exercise 11.6 |

The production-readiness-review skill is in the repository's top-level
`skills/` folder.

## Run

The scripts import `ch05/notes_api.py`, so run them from the repository
root (or your workspace root) with the Chapter 4 virtual environment
active:

```bash
python3 ch11/probe.py
# 100,000-char title + 5 MB body: 201
# GET /notes response size: 5100127 bytes
# GET /health: 404
# GET /docs: 200
```

After the health endpoint, the third line reads `GET /health: 200`.
After Exercise 11.3, the first line reads `422` and the response size
drops to 2 bytes. The probe uses a temporary database and never touches
`ch05/notes.db`.

To use the permissions profile, merge `safety/settings.json` into your
workspace's `.claude/settings.json`. Run `safety/setup-tidy-trap.sh`
only for the experiment; it creates `~/cc-scratch/tidy`.
