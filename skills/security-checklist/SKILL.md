---
name: security-checklist
description: Run a focused security review of a code change across input validation, authn/z, secrets, dependencies, and data exposure. Output a yes/no checklist plus one concrete patch per issue.
---

## Purpose

Make security review repeatable on AI-generated code. Catch the small set of issues that actually appear: input handling, authz, secret leaks, dependency risk, and over-broad data exposure.

## When to use

- Before merging any change that touches: a request handler, an auth path, a database query, an external API call, or a secret.
- Before tagging a release.
- During the production-readiness pass (in conjunction with `production-readiness-review`).

Skip when: the diff is documentation-only.

## Body

For each item, answer **yes** (verified safe) or **no** (write the smallest patch).

1. **Input validation** — every external input (path param, query, body, header) parsed by a schema before use.
2. **Authn/z** — every protected handler checks identity *and* authorization on the resource being acted on (not just "user is logged in").
3. **Secrets** — no API keys, tokens, passwords, or private URLs in source, configs committed to git, or logs.
4. **Injection** — all SQL via parameterised queries; all shell-out via argument arrays, never string concatenation; all template rendering escapes by default.
5. **Data exposure** — list/get endpoints filter to the caller's tenant/owner; error responses do not echo internal state (stack traces, raw SQL, secrets).
6. **Dependencies** — no new direct deps without an audit; lockfile committed.
7. **Rate limits / abuse** — the handler has a rate-limit story (even if it's "behind the gateway").
8. **Logging** — no PII / secrets in logs; log volume bounded.

## Inputs

- A diff or a focused folder.
- The framework / runtime in use.
- The trust boundary the change crosses (public, internal, batch, etc.).

## Outputs

A markdown checklist:

```markdown
- [yes/no] 1. Input validation — <evidence or smallest patch>
- [yes/no] 2. Authn/z — ...
... (8 items)
```

End with: `Verdict: SAFE / UNSAFE — <one-line rationale>`.

## Worked example

Input: a new `POST /notes` route that reads `request.json()` directly.

Output excerpt:

```markdown
- [no] 1. Input validation — body parsed without a schema; an oversized payload could OOM.
  Smallest patch: parse with `NoteIn = z.object({ title: z.string().min(1).max(200), body: z.string().max(10000) })`.
- [yes] 2. Authn/z — handler is behind the existing auth middleware; ownership not relevant (notes are user-scoped at write time).
- [yes] 3. Secrets — none introduced.
- [yes] 4. Injection — uses better-sqlite3 prepared statements.
...
Verdict: UNSAFE — apply patch in (1) before merge.
```
