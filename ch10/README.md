# Chapter 10: Extending Claude Code with Hooks, MCP and Multi-Agent Workflows

In this chapter, you add a PreToolUse hook that blocks Claude's commits while
the Notes API smoke test fails, and a Git pre-commit hook for the commits you
make yourself. You connect GitHub through MCP with a least-privilege token
kept in an environment variable, run the smoke test on four modules with
parallel subagents, and package the skill and hook as a plugin in a local
marketplace.

Files under `.claude/` mirror where they go in your `claude-code-projects`
workspace. The hook needs the `notes-api-smoke` skill from Chapter 9 at
`.claude/skills/notes-api-smoke/` in the same workspace; this folder doesn't
repeat it. The `team-tools/` folder is the plugin marketplace that the chapter
builds in `~/team-tools`, outside the workspace.

## Files

| File | What it is | Section | Copy it to |
|---|---|---|---|
| `.claude/hooks/guard.py` | PreToolUse hook: blocks `git commit` while the smoke test fails | Writing the hook script | `.claude/hooks/guard.py` |
| `.claude/settings.json` | Project settings that register the hook | Registering the hook | `.claude/settings.json` (merge the `hooks` section into yours) |
| `git-hooks/pre-commit` | Git hook that runs the same smoke test | Claude Code hooks versus Git hooks | `.git/hooks/pre-commit`, then `chmod +x` |
| `.mcp.json` | GitHub MCP server; the token comes from `${GITHUB_PAT}` | Adding the server without committing the token | `.mcp.json` at the workspace root |
| `mcp-run.md` | The brief for the one scoped MCP action | Running one scoped action | `ch10/mcp-run.md` (replace `YOUR-USER`) |
| `.claude/agents/smoke-runner.md` | Subagent that runs one smoke test and reports it | Subagents | `.claude/agents/smoke-runner.md` |
| `team-tools/.claude-plugin/marketplace.json` | Local marketplace catalog | Sharing it through a marketplace | `~/team-tools/.claude-plugin/marketplace.json` |
| `team-tools/notes-guardrails/.claude-plugin/plugin.json` | Plugin manifest | Packaging it all as a plugin | `~/team-tools/notes-guardrails/.claude-plugin/plugin.json` |
| `team-tools/notes-guardrails/hooks/hooks.json` | The plugin's hook registration, using `${CLAUDE_PLUGIN_ROOT}` | Packaging it all as a plugin | `~/team-tools/notes-guardrails/hooks/hooks.json` |
| `team-tools/notes-guardrails/hooks/guard.py` | Copy of `guard.py` | Packaging it all as a plugin | `~/team-tools/notes-guardrails/hooks/guard.py` |
| `team-tools/notes-guardrails/skills/notes-api-smoke/` | Copy of the Chapter 9 skill (`SKILL.md`, `smoke.py`) | Packaging it all as a plugin | `~/team-tools/notes-guardrails/skills/notes-api-smoke/` |
| `.claude/hooks/format_python.py` | PostToolUse hook that runs `ruff format` on edited Python files | Exercise 10.1 | `.claude/hooks/format_python.py` |
| `solutions/ex10.1/.claude/settings.json` | Settings with the PostToolUse group added | Exercise 10.1 | `.claude/settings.json` |
| `solutions/ex10.2/settings.deny-rules.json` | Settings with deny rules for the golden master (step 1) | Exercise 10.2 | `.claude/settings.json` |
| `solutions/ex10.2/.claude/hooks/protect_golden.py` | PreToolUse hook that blocks edits to `golden.json` and `test_pricing.py` (step 2) | Exercise 10.2 | `.claude/hooks/protect_golden.py` |
| `solutions/ex10.2/.claude/settings.json` | Settings that register `protect_golden.py` for `Edit\|Write` | Exercise 10.2 | `.claude/settings.json` |
| `solutions/ex10.5/notes-guardrails/agents/smoke-runner.md` | The subagent, changed to use the plugin's skill | Exercise 10.5 | `~/team-tools/notes-guardrails/agents/smoke-runner.md` |
| `solutions/ex10.5/notes-guardrails/.claude-plugin/plugin.json` | Manifest bumped to 1.1.0 | Exercise 10.5 | `~/team-tools/notes-guardrails/.claude-plugin/plugin.json` |

No file here contains a token. `.mcp.json` refers to `${GITHUB_PAT}`, which
Claude Code reads from your environment; set it with
`read -s GITHUB_PAT && export GITHUB_PAT` before you start `claude`.

## How to test

Activate a virtual environment with FastAPI and uvicorn installed, and run
these commands from the root of a Git clone that has the Notes API at
`ch05/notes_api.py` (your workspace, or this repository). The plugin copy of
`guard.py` is used here because it has the skill next to it; in your
workspace, use `.claude/hooks/guard.py` instead.

```bash
G=ch10/team-tools/notes-guardrails/hooks/guard.py
echo '{"tool_input": {"command": "git status"}}' | python3 $G; echo "exit $?"
echo '{"tool_input": {"command": "git commit -m test"}}' | python3 $G; echo "exit $?"
```

Both print `exit 0`. Now plant the bug from Chapter 9 (change the delete
route's `status_code=204` to `200` in `ch05/notes_api.py`) and run the second
command again. It prints `Commit blocked: ...`, the smoke-test output with
`FAIL  delete note (200)`, and `exit 2`. Undo the bug with
`git restore ch05/notes_api.py`.

Check that every JSON file parses:

```bash
find ch10 -name '*.json' -exec python3 -m json.tool {} \; > /dev/null && echo OK
```

The rest of the chapter (`/hooks`, the MCP connection, subagents, worktrees,
`claude plugin validate` and `claude plugin install`) needs Claude Code and,
for MCP, a GitHub token; follow the steps in the chapter.
