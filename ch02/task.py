"""Task Manager CLI (Python 3.11, stdlib only).

Commands:
  task add "<text>"
  task list [--status open|done]
  task done <id>
  task delete <id>

Persistence: tasks.json in CWD.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

DB = Path("tasks.json")


def _load() -> list[dict]:
    if not DB.exists():
        return []
    try:
        return json.loads(DB.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        print("error: tasks.json is corrupt", file=sys.stderr)
        sys.exit(2)


def _save(rows: list[dict]) -> None:
    DB.write_text(json.dumps(rows, indent=2), encoding="utf-8")


def _next_id(rows: list[dict]) -> int:
    return (max((r["id"] for r in rows), default=0)) + 1


def cmd_add(args: argparse.Namespace) -> int:
    text = args.text.strip()
    if not text:
        print("error: text must not be empty", file=sys.stderr)
        return 1
    rows = _load()
    row = {
        "id": _next_id(rows),
        "status": "open",
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "text": text,
    }
    rows.append(row)
    _save(rows)
    print(f"Added task #{row['id']}: {row['text']}")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    rows = _load()
    if args.status:
        rows = [r for r in rows if r["status"] == args.status]
    if not rows:
        print("(no tasks)")
        return 0
    print(f"{'id':>3}  {'status':<6}  {'created_at':<25}  text")
    for r in rows:
        print(f"{r['id']:>3}  {r['status']:<6}  {r['created_at']:<25}  {r['text']}")
    return 0


def cmd_done(args: argparse.Namespace) -> int:
    rows = _load()
    for r in rows:
        if r["id"] == args.id:
            r["status"] = "done"
            _save(rows)
            print(f"Marked #{r['id']} as done")
            return 0
    print(f"No task with id {args.id}", file=sys.stderr)
    return 1


def cmd_delete(args: argparse.Namespace) -> int:
    rows = _load()
    new_rows = [r for r in rows if r["id"] != args.id]
    if len(new_rows) == len(rows):
        print(f"No task with id {args.id}", file=sys.stderr)
        return 1
    _save(new_rows)
    print(f"Deleted #{args.id}")
    return 0


class _Parser(argparse.ArgumentParser):
    """Exit with 1 (user error) on bad arguments, not argparse's 2."""

    def error(self, message: str) -> None:
        self.print_usage(sys.stderr)
        print(f"{self.prog}: error: {message}", file=sys.stderr)
        raise SystemExit(1)


def main(argv: list[str] | None = None) -> int:
    p = _Parser(prog="task")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add")
    p_add.add_argument("text")
    p_add.set_defaults(fn=cmd_add)

    p_list = sub.add_parser("list")
    p_list.add_argument("--status", choices=["open", "done"])
    p_list.set_defaults(fn=cmd_list)

    p_done = sub.add_parser("done")
    p_done.add_argument("id", type=int)
    p_done.set_defaults(fn=cmd_done)

    p_del = sub.add_parser("delete")
    p_del.add_argument("id", type=int)
    p_del.set_defaults(fn=cmd_delete)

    args = p.parse_args(argv)
    try:
        return args.fn(args)
    except Exception as exc:  # internal error
        print(f"internal error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
