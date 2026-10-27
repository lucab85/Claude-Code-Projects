#!/usr/bin/env python3
"""Word-count CLI."""

import argparse
import sys


class UserErrorParser(argparse.ArgumentParser):
    """Argument parser that exits with 1, not 2, on usage errors."""

    def error(self, message):
        """Print usage and the error to stderr, then exit with 1."""
        self.print_usage(sys.stderr)
        print(f"{self.prog}: error: {message}", file=sys.stderr)
        raise SystemExit(1)


def count_words(path):
    """Return the number of words in a text file."""
    with open(path, encoding="utf-8") as f:
        return len(f.read().split())


def main():
    """Parse arguments and run the subcommand."""
    parser = UserErrorParser(description="Count things in files")
    subparsers = parser.add_subparsers(dest="command", required=True)

    words_parser = subparsers.add_parser("words", help="Count words in a file")
    words_parser.add_argument("file", help="Path to a text file")

    args = parser.parse_args()

    try:
        print(count_words(args.file))
    except FileNotFoundError:
        print(f"error: file not found: {args.file}", file=sys.stderr)
        raise SystemExit(1)
    except (IsADirectoryError, PermissionError, UnicodeDecodeError) as exc:
        print(f"error: cannot read {args.file}: {exc}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"internal error: {exc}", file=sys.stderr)
        raise SystemExit(2)
