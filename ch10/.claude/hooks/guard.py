#!/usr/bin/env python3
"""PreToolUse hook: block git commit while the smoke test fails."""
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SMOKE = HERE.parent / "skills" / "notes-api-smoke" / "smoke.py"
ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR", Path.cwd()))
API = os.environ.get("NOTES_API", "ch05/notes_api.py")
PORT = "8199"


def main():
    """Exit 0 to allow the command, or 2 to block it."""
    event = json.load(sys.stdin)
    command = event.get("tool_input", {}).get("command", "")
    if "git commit" not in command:
        return 0
    changed = subprocess.run(
        ["git", "diff", "HEAD", "--name-only"], cwd=ROOT,
        capture_output=True, text=True).stdout.split()
    if API not in changed:
        return 0
    result = subprocess.run(
        [sys.executable, str(SMOKE), str(ROOT / API), PORT],
        capture_output=True, text=True)
    if result.returncode == 0:
        return 0
    print(f"Commit blocked: the smoke test fails for {API}.\n"
          f"{result.stdout}Fix the failures, then commit again.",
          file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
