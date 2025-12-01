import argparse
import json
import typing as t
from enum import IntEnum, StrEnum, auto
from pathlib import Path

from cogapp import Cog

BASE_DIR = Path(__file__).parent.parent


class Lang(StrEnum):  # noqa: D101
    PYTHON = auto()
    DART = auto()
    GO = auto()
    JULIA = auto()
    LOX = auto()
    MATLAB = auto()
    RUST = auto()


class State(IntEnum):  # noqa: D101
    NOT = 0
    PARTIAL = 1
    DONE = 2


ICONS = {
    State.NOT: ":x:",
    State.PARTIAL: ":white_circle:",
    State.DONE: ":white_check_mark:",
}
MIN_WIDTH = max(len(icon) for icon in ICONS.values())

HEADER = f"""\
# Solution Tracker
{ICONS[State.NOT]} - Not complete
{ICONS[State.PARTIAL]} - Partially complete
{ICONS[State.DONE]} - Complete
"""

DATA_T: t.TypeAlias = dict[str, list[State]]


def build_table(data: DATA_T, n_days: int) -> str:  # noqa: D103
    header = f"|    |{'|'.join(la.title().center(MIN_WIDTH+2) for la in Lang)}|"
    header = header.replace("Matlab", "MATLAB")  # Special case name

    sub_div = f":{'-'*MIN_WIDTH}:|"
    divider = f"|----|{sub_div*len(Lang)}"

    rows = []
    for day in range(n_days):
        rows.append(
            f"|{day+1:^4}|{'|'.join(ICONS[data[la][day]].center(MIN_WIDTH+2) for la in Lang)}|"
        )

    all_rows = "\n".join(rows)
    return f"{header}\n{divider}\n{all_rows}"


def ensure_lang(data: DATA_T, n_days: int) -> DATA_T:
    """Ensure that the data table contains all the languages defined by `Lang`."""
    for lang in Lang - data.keys():
        data[lang] = [State.NOT] * n_days

    return data


def parse_progress_json(filepath: Path, n_days: int) -> DATA_T:
    """
    Parse the progress data from the provided README file.

    If a new language has been added since the README file was generated, an empty column for the
    new language will be created.
    """
    with filepath.open("r") as f:
        first_line = f.readline()

    if first_line.startswith("<!--"):
        data_table = json.loads(
            first_line.rstrip().removeprefix("<!--").removesuffix("-->").strip()
        )
        data_table = ensure_lang(data_table, n_days=n_days)
    else:
        data_table = {lang.value: ([State.NOT] * n_days) for lang in Lang}

    return data_table  # type: ignore[no-any-return]


def build_summary_table() -> str:
    """Build a completion stats summary table from the data in each year's README."""
    col_width = 8
    header = f"|        |{'|'.join(la.title().center(col_width+2) for la in Lang)}|"
    header = header.replace("Matlab", "MATLAB")  # Special case name

    sub_div = f":{'-'*col_width}:|"
    divider = f"|--------|{sub_div*len(Lang)}"

    rows = []
    for filepath in sorted(BASE_DIR.glob("2*/README.md"), key=lambda x: x.parent):
        year = filepath.parent.name

        # Starting in 2025, the event is 12 long days rather than the historical 25
        if int(year) >= 2025:
            n_days = 12
        else:
            n_days = 25

        data = parse_progress_json(filepath, n_days=n_days)

        row = []
        for la in Lang:
            partial = sum((day == State.PARTIAL) for day in data[la])
            full = sum((day == State.DONE) for day in data[la])

            row.append(f"`{full:2}, {partial:2}`")

        rows.append(f"| `{year}` |{'|'.join(col.center(col_width+2) for col in row)}|")

    all_rows = "\n".join(rows)
    return f"{header}\n{divider}\n{all_rows}"


def main() -> None:  # noqa: D103
    parser = argparse.ArgumentParser()
    parser.add_argument("year", type=int)
    parser.add_argument("day", type=int)
    parser.add_argument("lang", type=Lang)
    parser.add_argument("state", choices=("not", "partial", "done"))

    args = parser.parse_args()

    # Starting in 2025, the event is 12 long days rather than the historical 25
    if args.year >= 2025:
        n_days = 12
    else:
        n_days = 25

    filepath = BASE_DIR / f"{args.year}" / "README.md"
    data_table = parse_progress_json(filepath, n_days=n_days)

    data_table[args.lang][args.day - 1] = State[args.state.upper()]

    with filepath.open("w") as f:
        f.write(f"<!-- {json.dumps(data_table)} -->\n")
        f.write(f"{HEADER}\n\n")
        f.write(f"{build_table(data_table, n_days=n_days)}\n")
    print(f"Puzzle status updated: ({args.year}, {args.day}, {args.lang}, {args.state})")

    # Update the base README with the new status using Cog & a dummy sys.argv
    cog = Cog()
    cog.main(["", "-r", str((BASE_DIR / "README.MD").resolve())])


if __name__ == "__main__":
    main()
