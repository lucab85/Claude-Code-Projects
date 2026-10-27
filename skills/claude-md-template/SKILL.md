---
name: claude-md-template
description: Author a behavior-changing CLAUDE.md for any repository. Outputs a ≤80-line file with five required sections, each line earning its place.
---

## Purpose

Produce a `CLAUDE.md` that materially changes Claude's behavior on every subsequent prompt in the repo. Not a README. Not an ABOUT.md. A behavior file.

## When to use

- Onboarding a new repo to AI-paired coding.
- After a refactor changes the project's stack or conventions.
- When you keep re-explaining the same context in every prompt.

Skip when: the repo has < 100 LoC, or you do not own the conventions.

## Body

1. **Read the repo first.** Use `ls` and read the top-level package manifest before drafting.
2. Draft five H1 sections in order:
   - `# Stack` — languages, package managers, runtime versions.
   - `# Conventions` — naming, layout, lint/format rules.
   - `# Commands` — exact commands for build / test / run / lint.
   - `# Do-not` — hard-won rules (e.g., "never add deps without asking").
   - `# Glossary` — domain terms only this team uses.
3. **Trim test**: for each line, ask "would deleting this line change a future Claude response?" If no, delete.
4. Cap the file at **80 lines**.
5. Commit it at repo root.

## Inputs

- Working directory of a repo (any language).
- Optionally: a list of three pain points the author keeps re-explaining.

## Outputs

- A single `CLAUDE.md` file at repo root.
- ≤ 80 lines.
- Contains exactly five H1 sections in the order above.
- Every line is a behavior-changing instruction or a domain term definition.

## Worked example

Input: a TypeScript Hono API with better-sqlite3.

Output excerpt:

```markdown
# Stack
TypeScript on Node 20. Hono. better-sqlite3. No ORM.

# Conventions
- One route handler per file under `src/routes/`.
- Always validate request bodies with Zod schemas in `src/schemas/`.
- Use ISO 8601 UTC timestamps everywhere (`new Date().toISOString()`).

# Commands
- Run dev: `npm run dev`
- Test:    `npm test`
- Lint:    `npm run lint`

# Do-not
- Do not add ORM dependencies. We use raw better-sqlite3.
- Do not catch errors silently. Surface them with a 5xx.

# Glossary
- "card" = a single Notes-API note (legacy term).
```
