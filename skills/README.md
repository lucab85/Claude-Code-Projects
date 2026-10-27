# Skills library

Twelve reusable Claude Code skills by Luca Berton, used in *Chapter 9* and later chapters of *Claude Code Projects*.

**Licensed MIT, so you can reuse them in commercial work.** See [`LICENSE`](LICENSE).

## What is a skill?

A skill is a folder with a `SKILL.md` file: YAML frontmatter (`name`, `description`) followed by Markdown instructions. Claude Code lists every skill it discovers, loads one when your request matches its description, and lets you run it by name as `/<name>`.

## The 12 skills

| Skill | Purpose |
|---|---|
| [`best-of-n`](best-of-n/SKILL.md) | Produce N independent candidate implementations, score them and pick the winner. |
| [`claude-md-template`](claude-md-template/SKILL.md) | Write a short, project-aware `CLAUDE.md` with the five recommended sections. |
| [`code-review`](code-review/SKILL.md) | Review a diff as if it were a stranger's pull request, with ranked, severity-tagged findings. |
| [`documentation-generation`](documentation-generation/SKILL.md) | Produce `HANDOFF.md` and `ARCHITECTURE.md` from a diff and the resulting source. |
| [`git-workflow`](git-workflow/SKILL.md) | Turn a working-tree diff into atomic Conventional Commits and a pull request description. |
| [`mcp-context-brief`](mcp-context-brief/SKILL.md) | Prepare a one-page context brief before connecting an MCP tool (Jira, Slack, GitHub, Drive). |
| [`production-readiness-review`](production-readiness-review/SKILL.md) | Report on the five production-readiness axes with evidence and a Go / No-Go. |
| [`refactor`](refactor/SKILL.md) | Refactor a module under hard written constraints and return a unified diff. |
| [`release-notes`](release-notes/SKILL.md) | Turn a Git range or changelog into release notes grouped by audience. |
| [`release-readiness`](release-readiness/SKILL.md) | Walk a change or release branch through a 12-item readiness checklist. |
| [`security-checklist`](security-checklist/SKILL.md) | Review a change for input validation, auth, secrets, dependencies and more. |
| [`test-generation`](test-generation/SKILL.md) | Generate a runnable test suite covering happy paths, error paths and edge cases. |

## How to install

Claude Code discovers project skills in `.claude/skills/` at the root of the folder where you start it (and personal skills in `~/.claude/skills/`). Copy only the skills you need:

```bash
mkdir -p .claude/skills
cp -r <book-code>/skills/code-review .claude/skills/
```

Replace `<book-code>` with the folder where you cloned this repository. Start a new Claude Code session, then type `/skills` to check the skill is listed.

> **Name clash:** Claude Code has a built-in `/code-review` command. If you install the library's `code-review` skill, copy it under a different folder name and change the `name:` line to match, for example `stranger-review`.

## How each skill is structured

Every `SKILL.md` follows the same six-section shape:

- **Frontmatter**: `name` and a one-line `description` that tells Claude Code when to use it
- **Purpose**: what the skill does
- **When to use**: concrete trigger scenarios
- **Body**: the instructions Claude Code follows
- **Inputs**: what you supply
- **Outputs**: what you get back, plus a short worked example

Every skill is path-agnostic: none depends on this repository's layout, so you can drop it into any codebase unchanged.
