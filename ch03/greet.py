#!/usr/bin/env python3
"""Greeting CLI."""

import argparse


def main():
    parser = argparse.ArgumentParser(description="Greeting tool")
    subparsers = parser.add_subparsers(dest="command")

    hello_parser = subparsers.add_parser("hello", help="Greet a person")
    hello_parser.add_argument("name", help="Name to greet")
    hello_parser.add_argument(
        "--upper", action="store_true", help="Uppercase the greeting"
    )

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        raise SystemExit(1)

    message = f"Hello, {args.name}!"
    if args.upper:
        message = message.upper()
    print(message)


if __name__ == "__main__":
    main()
