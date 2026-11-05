# Production readiness: Notes API (Chapter 4 service)

Produced with the `release-readiness` skill (`skills/release-readiness`)
against the Chapter 4 Notes API. This is the report you audit in
Exercise 11.1. Don't fix it: its mistakes are the point of the exercise.

Verdict: **NO-GO** (3 blockers).

| # | Item | Status | Evidence | Action if NOT |
|---|---|---|---|---|
| 1 | Secrets hygiene | ✓ | `.env` ignored; no keys in git history (`git log -p \| grep -iE 'api[_-]?key'`). | — |
| 2 | AuthN / AuthZ | ✗ | No auth on `/tasks` endpoints. | Add API-key middleware before public exposure. |
| 3 | Input validation | ✓ | Pydantic models reject empty `title`. | — |
| 4 | Error budgets | ✗ | No SLO defined. | Pick a 99.5% target for `/tasks`; alert on 5xx > 0.5%. |
| 5 | Idempotency | △ | `POST /tasks` not idempotent; client could double-submit. | Add `Idempotency-Key` header. |
| 6 | Observability | ✗ | No structured logs; no traces. | Add `structlog` + OTLP exporter. |
| 7 | Performance | ✓ | p95 < 50ms on 1k tasks (smoke). | — |
| 8 | Backwards compatibility | n/a | First release. | — |
| 9 | Disaster recovery | △ | SQLite file; no backup. | Document daily snapshot to S3. |
| 10 | Rollback | ✓ | Container image tagged per commit; previous tag re-deployable. | — |
| 11 | Permission scope | ✓ | Container runs as non-root UID 1000. | — |
| 12 | Human review | ✓ | This report counter-signed by senior eng. | — |
