#!/usr/bin/env python3
"""PreToolUse hook: block edits to the Chapter 8 golden master and tests."""
import json
import sys

PROTECTED = ("golden.json", "test_pricing.py")

event = json.load(sys.stdin)
path = event.get("tool_input", {}).get("file_path", "")
if path.endswith(PROTECTED):
    print("golden.json and the tests are the referee; change the code instead",
          file=sys.stderr)
    sys.exit(2)
