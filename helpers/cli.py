import argparse
import sys
from collections import abc

from helpers.common import BASE_DIR, validate_puzzle_date
from helpers.init_puzzle import available_langs, init_puzzle_day
from helpers.run_puzzle import RUNNERS, run_puzzle
from helpers.update_progress import Lang, State, set_progress


def _add_date_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("year", type=int)
    parser.add_argument("day", type=int)


def _init(args: argparse.Namespace, extra_args: list[str]) -> int:
    try:
        created = init_puzzle_day(args.year, args.day, args.lang)
    except FileExistsError as e:
        print(f"aoc: {e}", file=sys.stderr)
        return 1

    for path in created:
        print(f"Created {path.relative_to(BASE_DIR).as_posix()}")

    return 0


def _set_prog(args: argparse.Namespace, extra_args: list[str]) -> int:
    set_progress(args.year, args.day, args.lang, State[args.state.upper()])
    return 0


def _run(args: argparse.Namespace, extra_args: list[str]) -> int:
    return run_puzzle("run", args.year, args.day, args.lang, extra_args)


def _test(args: argparse.Namespace, extra_args: list[str]) -> int:
    return run_puzzle("test", args.year, args.day, args.lang, extra_args)


def build_parser() -> argparse.ArgumentParser:
    """
    Build the `aoc` argument parser.

    Each subcommand sets `func`, a callable taking the parsed arguments & any arguments given after
    `--`, and returning an exit code. Subcommands that accept arguments after `--` also set
    `passthrough=True`.
    """
    parser = argparse.ArgumentParser(prog="aoc", description="Advent of Code helpers.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Initialize a puzzle day's folder")
    _add_date_args(init_parser)
    init_parser.add_argument(
        "--lang",
        nargs="+",
        choices=available_langs(),
        default=["python"],
        help="Language template(s) to create (default: python)",
    )
    init_parser.set_defaults(func=_init)

    progress_parser = subparsers.add_parser("set-prog", help="Set a puzzle day's completion state")
    _add_date_args(progress_parser)
    progress_parser.add_argument("lang", type=Lang, choices=list(Lang))
    progress_parser.add_argument("state", choices=[state.name.lower() for state in State])
    progress_parser.set_defaults(func=_set_prog)

    for name, func, help_text in (
        ("run", _run, "Run a puzzle day's solution"),
        ("test", _test, "Run a puzzle day's tests"),
    ):
        action_parser = subparsers.add_parser(
            name,
            help=help_text,
            epilog="Arguments after `--` are passed through to the underlying command.",
        )
        _add_date_args(action_parser)
        action_parser.add_argument(
            "--lang",
            nargs="+",
            choices=sorted(RUNNERS),
            default=["python"],
            help="Language(s) to use (default: python)",
        )
        action_parser.set_defaults(func=func, passthrough=True)

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

    if extra_args and not getattr(args, "passthrough", False):
        parser.error(f"arguments after `--` are not supported by `{args.command}`")

    if hasattr(args, "year") and hasattr(args, "day"):
        try:
            validate_puzzle_date(args.year, args.day)
        except ValueError as e:
            parser.error(str(e))

    sys.exit(args.func(args, extra_args))


if __name__ == "__main__":
    main()
