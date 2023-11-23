import argparse
import json
import typing as t
from enum import IntEnum, StrEnum, auto
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class Lang(StrEnum):  # noqa: D101
    PYTHON = auto()
    MATLAB = auto()
    RUST = auto()
    LOX = auto()
    JULIA = auto()
    GO = auto()


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


def build_table(data: DATA_T) -> str:  # noqa: D103
    header = f"|    |{'|'.join(la.title().center(MIN_WIDTH+2) for la in Lang)}|"
    header = header.replace("Matlab", "MATLAB")  # Special case name

    sub_div = f":{'-'*MIN_WIDTH}:|"
    divider = f"|----|{sub_div*len(Lang)}"

    rows = []
    for day in range(25):
        rows.append(
            f"|{day+1:^4}|{'|'.join(ICONS[data[la][day]].center(MIN_WIDTH+2) for la in Lang)}|"
        )

    return f"{header}\n{divider}\n{'\n'.join(rows)}"


def ensure_lang(data: DATA_T) -> DATA_T:
    """Ensure that the data table contains all the languages defined by `Lang`."""
    for lang in Lang - data.keys():
        data[lang] = [State.NOT] * 25

    return data


def main() -> None:  # noqa: D103
    parser = argparse.ArgumentParser()
    parser.add_argument("year", type=int)
    parser.add_argument("day", type=int)
    parser.add_argument("lang", type=Lang)
    parser.add_argument("state", choices=("not", "partial", "done"))

    args = parser.parse_args()

    filepath = BASE_DIR / f"{args.year}" / "README.md"
    with filepath.open("r") as f:
        first_line = f.readline()

    if first_line.startswith("<!--"):
        data_table = json.loads(
            first_line.rstrip().removeprefix("<!--").removesuffix("-->").strip()
        )
        data_table = ensure_lang(data_table)
    else:
        data_table = {lang.value: ([State.NOT] * 25) for lang in Lang}

    data_table[args.lang][args.day - 1] = State[args.state.upper()]

    with filepath.open("w") as f:
        f.write(f"<!-- {json.dumps(data_table)} -->\n")
        f.write(f"{HEADER}\n\n")
        f.write(f"{build_table(data_table)}\n")


if __name__ == "__main__":
    main()
