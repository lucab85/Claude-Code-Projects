---
name: release-readiness
description: Walk a code change (or full release branch) through a 12-item production-readiness checklist and produce a go / no-go report with concrete remediations.
---

## Purpose

Stop "it works on my machine" releases. Force a deliberate pass over the dimensions that bite the night a release goes out: security, reliability, observability, performance, and disaster recovery.

This skill is the natural follow-up to `code-review` and `security-checklist`: those find local defects in a diff; `release-readiness` evaluates whether the **system** is safe to ship.

## When to use

- Before tagging a release.
- Before merging a long-lived branch into `main`.
- Before opening a PR that touches infra, secrets, schema, or external integrations.
- As the closing review in any cohort's Part 10 (Production Readiness).

Skip when: the change is documentation-only or a typo fix with no executable surface.

## Body

Walk the 12 items in order. For each: state the **finding** (one sentence), the **evidence** (a file / log / metric), and the **remediation** (concrete next action). End with a one-line go / no-go.

1. **Secrets hygiene** — no credentials in git history, env files, or logs.
2. **Authentication & authorization** — every privileged path has a matching test or audit.
3. **Input validation** — every external input has a schema and a rejection path.
4. **Error budgets & retries** — bounded retries, jittered backoff, no infinite loops on transient errors.
5. **Idempotency** — write paths can be safely retried.
6. **Observability** — structured logs, request IDs, at least one alert per critical user journey.
7. **Performance budgets** — p95 latency and memory under documented ceiling for the change.
8. **Backwards compatibility** — schema / API changes are additive or feature-flagged.
9. **Disaster recovery** — backup + restore drill within the last 30 days; runbook linked from the PR.
10. **Rollback plan** — `git revert <sha>` is safe, or there's a documented data migration backout.
11. **Permission scope** — agents and services use least-privilege tokens, not personal credentials.
12. **Human review** — at least one named reviewer for the change, distinct from the author.

Output is a single markdown report — never a free-form essay.

## Inputs

- The release branch name or commit range (`main..release/2026-05`).
- The target environment (`staging` / `prod`).
- Links to dashboards / alerts / runbooks if available.

## Outputs

```text
## Release readiness — <branch> -> <env>

| # | Item | Finding | Evidence | Remediation |
|---|---|---|---|---|
| 1 | Secrets hygiene | … | … | … |
| 2 | AuthN/Z | … | … | … |
| … |
| 12 | Human review | … | … | … |

**Verdict**: GO / NO-GO  
**Blockers**: <list item numbers that are NO-GO>
```

## Worked example

Input: `main..release/2026-05` on a FastAPI service.

Excerpt of output:

```text
| 1 | Secrets hygiene | PASS | `gitleaks --no-banner` returns 0; `.env.example` only | none |
| 4 | Error budgets | FAIL | `httpx.AsyncClient` has no timeout in 3 call sites | Add `timeout=10.0` to clients in app/clients/*.py |
| 9 | Disaster recovery | WARN | Last restore drill 2026-03-14 (>30 d) | Schedule a drill before tag |

Verdict: NO-GO
Blockers: 4
```
