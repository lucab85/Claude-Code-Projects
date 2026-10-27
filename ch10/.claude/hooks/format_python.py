#!/usr/bin/env python3
"""PostToolUse hook: format a Python file after Claude edits it."""
import json
import shutil
import subprocess
import sys

event = json.load(sys.stdin)
path = event.get("tool_input", {}).get("file_path", "")
if path.endswith(".py") and shutil.which("ruff"):
    subprocess.run(["ruff", "format", "--quiet", path], check=False)
