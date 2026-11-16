import subprocess
import sys
from collections import abc
from dataclasses import dataclass
from string import Template

from helpers.common import BASE_DIR, puzzle_dir


@dataclass(frozen=True)
class LangRunner:
    """
    How to run and test one language's solution for a puzzle day.

    Every string is a `string.Template`, substituted with:
        * `${year}` - the 4-digit year
        * `${day}` - the zero-padded 2-digit day
        * `${day_dir}` - the day folder, relative to the repo root (e.g. `2015/Day_01`)
        * `${python}` - the running Python interpreter

    Commands are run from the repo root, which is also the Cargo workspace & Go module root.

    Attributes:
        marker: A file, relative to the day folder, whose presence means the day has a solution in
            this language.
        run: The command used to run the solution.
        test: The command used to run the solution's tests, or `None` if the language has no test
            convention.
    """

    marker: str
    run: tuple[str, ...]
    test: tuple[str, ...] | None


# To support another language, add an entry keyed by its name (matching its folder in
# `helpers/templates/`, if it has one). Arguments given after `--` on the command line are appended
# to the end of the run or test command.
RUNNERS: dict[str, LangRunner] = {
    "python": LangRunner(
        marker="aoc_${year}_day${day}.py",
        run=("${python}", "${day_dir}/aoc_${year}_day${day}.py"),
        test=("${python}", "-m", "pytest", "${day_dir}"),
    ),
    "rust": LangRunner(
        marker="rust/Cargo.toml",
        run=("cargo", "run", "-q", "-p", "y${year}_d${day}"),
        test=("cargo", "test", "-q", "-p", "y${year}_d${day}"),
    ),
    "go": LangRunner(
        marker="go/main.go",
        run=("go", "run", "./${day_dir}/go"),
        test=("go", "test", "./${day_dir}/go"),
    ),
}


def build_command(
    lang: str, action: str, year: int, day: int, extra_args: abc.Sequence[str] = ()
) -> list[str]:
    """
    Build the command line for running (`action="run"`) or testing (`action="test"`) a solution.

    Raises `FileNotFoundError` if the day has no solution in `lang`, and `ValueError` if `lang` has
    no command for `action`.
    """
    runner = RUNNERS[lang]
    day_dir = puzzle_dir(year, day)
    mapping = {
        "year": f"{year}",
        "day": f"{day:02d}",
        "day_dir": day_dir.relative_to(BASE_DIR).as_posix(),
        "python": sys.executable,
    }

    marker = day_dir / Template(runner.marker).substitute(mapping)
    if not marker.exists():
        raise FileNotFoundError(
            f"No {lang} solution for {year} day {day}: missing "
            f"{marker.relative_to(BASE_DIR).as_posix()}"
        )

    template = runner.run if action == "run" else runner.test
    if template is None:
        raise ValueError(f"{lang} has no {action} command")

    return [Template(part).substitute(mapping) for part in template] + list(extra_args)


def run_puzzle(
    action: str, year: int, day: int, langs: abc.Iterable[str], extra_args: abc.Sequence[str] = ()
) -> int:
    """
    Run or test the given day's solution in each of `langs`, in order.

    Every language is attempted even if an earlier one fails. Returns the first nonzero exit code
    encountered, or `0` if all succeeded.
    """
    exit_code = 0
    for lang in langs:
        try:
            command = build_command(lang, action, year, day, extra_args)
        except (FileNotFoundError, ValueError) as e:
            print(f"aoc: {e}", file=sys.stderr)
            exit_code = exit_code or 1
            continue

        print(f"==> {lang}: {' '.join(command)}", file=sys.stderr)
        result = subprocess.run(command, cwd=BASE_DIR)
        exit_code = exit_code or result.returncode

    return exit_code
