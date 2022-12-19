import argparse
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

PUZZLE_FILES = (
    "puzzle_input.txt",
    "README.md",
    "sample_input.txt",
)

PY_BASE = """\
from pathlib import Path


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text()

    print(f"Part One: {...}")
    print(f"Part Two: {...}")
"""

TEST_BASE = '''\
from textwrap import dedent


SAMPLE_INPUT = dedent(
    """\\
    """
)
'''

PY_FILES = (
    "__init__.py",
    ("aoc_2022_day{:02d}.py", PY_BASE),
    ("test_day{:02d}.py", TEST_BASE),
)


def init_puzzle_day(year: int, day: int) -> None:  # noqa: D103
    year_dir = BASE_DIR / f"{year}"
    year_dir.mkdir(exist_ok=True)

    day_dir = year_dir / f"Day_{day:02d}"
    day_dir.mkdir(exist_ok=False)

    for filename in PUZZLE_FILES:
        (day_dir / filename).touch()

    for file in PY_FILES:
        if len(file) == 2:
            filename, contents = file
            filename = filename.format(day)
            (day_dir / filename).write_text(contents)
        else:
            filename = file.format(day)
            (day_dir / filename).touch()


def main() -> None:  # noqa: D103
    parser = argparse.ArgumentParser()
    parser.add_argument("year", type=int)
    parser.add_argument("day", type=int)

    args = parser.parse_args()
    init_puzzle_day(args.year, args.day)


if __name__ == "__main__":
    main()
