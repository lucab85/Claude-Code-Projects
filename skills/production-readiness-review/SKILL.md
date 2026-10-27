---
name: production-readiness-review
description: Score a project across the five production-readiness axes (security, observability, deployment, runbooks, rollback). Output a one-page report ending with a go/no-go verdict.
---

## Purpose

Convert "works on my laptop" into a defensible go / no-go decision. Forces honesty across the five axes that actually matter the first week in production.

## When to use

- Before promoting any project past a personal-prototype boundary.
- During tech-debt pruning to identify the smallest next step that materially raises the floor.
- As part of an interview or peer review of AI-generated work.

Skip when: the project is explicitly a throwaway script with a known one-shot use.

## Body

Run the project through each axis. For each, answer in one sentence: *would this hold up in production this week?* Then identify the single biggest risk and the single smallest next step.

Axes:

1. **Security** — input validation, authn/z, secret handling, dependency hygiene.
2. **Observability** — structured logs, request IDs, error signals, basic metrics.
3. **Deployment** — reproducible build, healthcheck endpoint, container/runtime story.
4. **Runbooks** — one page covering "common failure → first action".
5. **Rollback** — can the previous version be restored in < 15 minutes? Are migrations reversible?

Score each axis: **green** (acceptable for first-week production), **yellow** (one concrete action away), **red** (blocks shipping).

End with a go / no-go verdict and a ≤ 25-word rationale.

## Inputs

- Read access to the project source.
- Optional: target environment (cloud, on-prem, single-node, k8s).
- Optional: the SLA the project must meet.

## Outputs

A markdown report:

```markdown
# Production Readiness Report — <project>

## Security
- Status: <green/yellow/red>
- Biggest risk: <one sentence>
- Smallest next step: <concrete action, not "improve security">

## Observability
... (same shape)

## Deployment
...

## Runbooks
...

## Rollback
...

## Verdict
Go / No-Go: <choice>. Rationale: <≤ 25 words>.
```

One page. No prose between sections.

## Worked example

Input: a small Notes API (FastAPI + SQLite) developed in a 30-minute lab.

Output excerpt:

```markdown
## Security
- Status: yellow
- Biggest risk: no rate limiting on POST /notes; abuse vector for storage.
- Smallest next step: add `slowapi` middleware capped at 60/min/IP.

## Verdict
Go / No-Go: No-Go. Rationale: needs rate limiting and a healthcheck before any production exposure.
```
