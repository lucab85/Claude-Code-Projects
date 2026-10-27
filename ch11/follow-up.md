# Follow-up: Notes API readiness (ch05)

From readiness-report.md. Cheapest steps first.

| Axis | Step | Size (S/M/L) | Unblocks | Order |
|---|---|---|---|---|
| Observability | Add GET /health that opens a connection and runs SELECT 1, test-first | S | Removes Observability's biggest risk and gives Deployment a health check; Observability stays yellow until logging lands | 1 |
| Security | Limit titles to 200 and bodies to 10,000 characters on create and update (Exercise 11.3) | S | Closes the input-limits gap; Security stays red until authentication | 2 |
| Deployment | Freeze runtime dependencies into ch05/requirements.txt and document a run command without --reload (Exercise 11.6) | S | Deployment red to yellow | 3 |
| Runbooks | Write ch05/RUNBOOK.md: five failures, the first command for each, every command tried (Exercise 11.4) | S | Runbooks red to yellow | 4 |
| Rollback | Tag v1.0.0, back up notes.db before every deploy and run the rollback drill (Exercise 11.5) | S | Rollback yellow to green | 5 |
| Observability | Log one line per request with a request ID, method, path, status and duration | M | Observability yellow to green | 6 |
| Security | Require an API key header on every route, read from an environment variable | M | Security red to yellow | 7 |
| Security | Page GET /notes with limit and offset; turn off /docs outside development | M | Security yellow to green, with the steps above | 8 |
| Deployment | Add a container or service file that runs the pinned install | M | Deployment yellow to green | 9 |

## Done

- 1. GET /health added with test_health_reports_ok. 14 tests pass, the
  smoke test passes, and the probe prints `GET /health: 200`.
