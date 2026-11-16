import argparse
import sys
from collections import abc

from helpers.common import validate_puzzle_date
from helpers.run_puzzle import RUNNERS, run_puzzle


def _add_puzzle_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("year", type=int)
    parser.add_argument("day", type=int)
    parser.add_argument(
        "--lang",
        nargs="+",
        choices=sorted(RUNNERS),
        default=["python"],
        help="Language(s) to use (default: python)",
    )


def _run(args: argparse.Namespace, extra_args: list[str]) -> int:
    return run_puzzle("run", args.year, args.day, args.lang, extra_args)


def _test(args: argparse.Namespace, extra_args: list[str]) -> int:
    return run_puzzle("test", args.year, args.day, args.lang, extra_args)


def build_parser() -> argparse.ArgumentParser:
    """
    Build the `aoc` argument parser.

    Each subcommand sets `func`, a callable taking the parsed arguments & any arguments given after
    `--`, and returning an exit code.
    """
    parser = argparse.ArgumentParser(
        prog="aoc",
        description="Advent of Code helpers.",
        epilog="Arguments after `--` are passed through to the underlying run or test command.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run a puzzle day's solution")
    _add_puzzle_args(run_parser)
    run_parser.set_defaults(func=_run)

    test_parser = subparsers.add_parser("test", help="Run a puzzle day's tests")
    _add_puzzle_args(test_parser)
    test_parser.set_defaults(func=_test)

    return parser


def main(argv: abc.Sequence[str] | None = None) -> None:  # noqa: D103
    argv = list(sys.argv[1:] if argv is None else argv)

    # Split off pass-through arguments ourselves; argparse would otherwise try to parse them
    extra_args: list[str] = []
    if "--" in argv:
        split_idx = argv.index("--")
        argv, extra_args = argv[:split_idx], argv[split_idx + 1 :]

    parser = build_parser()
    args = parser.parse_args(argv)

    if hasattr(args, "year") and hasattr(args, "day"):
        try:
            validate_puzzle_date(args.year, args.day)
        except ValueError as e:
            parser.error(str(e))

    sys.exit(args.func(args, extra_args))


if __name__ == "__main__":
    main()
