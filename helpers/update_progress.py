import json
import typing as t
from collections import abc
from enum import IntEnum, StrEnum, auto
from pathlib import Path

from helpers.common import n_puzzle_days, validate_puzzle_date

BASE_DIR = Path(__file__).parent.parent


class Lang(StrEnum):  # noqa: D101
    PYTHON = auto()
    DART = auto()
    GO = auto()
    JULIA = auto()
    LOX = auto()
    MATLAB = auto()
    RUST = auto()


ALWAYS_SHOW: frozenset[Lang] = frozenset({Lang.PYTHON})

DISPLAY_NAME_OVERRIDE: dict[Lang, str] = {
    Lang.MATLAB: "MATLAB",
}


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


def active_langs(data_tables: abc.Iterable[DATA_T]) -> list[Lang]:
    """
    Determine which languages to emit a column for, in `Lang` definition order.

    A language is considered active if it's in `ALWAYS_SHOW`, or if at least one day in any of the
    provided data tables is not marked as `State.NOT`.
    """
    data_tables = list(data_tables)
    return [
        la
        for la in Lang
        if la in ALWAYS_SHOW
        or any(state != State.NOT for data in data_tables for state in data[la])
    ]


def build_table(data: DATA_T, n_days: int) -> str:  # noqa: D103
    langs = active_langs((data,))
    header = f"|    |{'|'.join(DISPLAY_NAME_OVERRIDE.get(la, la.title()).center(MIN_WIDTH+2) for la in langs)}|"  # noqa: E501

    sub_div = f":{'-'*MIN_WIDTH}:|"
    divider = f"|----|{sub_div*len(langs)}"

    rows = []
    for day in range(n_days):
        rows.append(
            f"|{day+1:^4}|{'|'.join(ICONS[data[la][day]].center(MIN_WIDTH+2) for la in langs)}|"
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
    yearly_data = {}
    for filepath in sorted(BASE_DIR.glob("2*/README.md"), key=lambda x: x.parent):
        year = filepath.parent.name
        n_days = n_puzzle_days(int(year))
        yearly_data[year] = parse_progress_json(filepath, n_days=n_days)

    # Columns must be consistent across all rows, so use the union of each year's active languages
    langs = active_langs(yearly_data.values())

    col_width = 8
    header = f"|        |{'|'.join(DISPLAY_NAME_OVERRIDE.get(la, la.title()).center(col_width+2) for la in langs)}|"  # noqa: E501

    sub_div = f":{'-'*col_width}:|"
    divider = f"|--------|{sub_div*len(langs)}"

    rows = []
    for year, data in yearly_data.items():
        row = []
        for la in langs:
            partial = sum((day == State.PARTIAL) for day in data[la])
            full = sum((day == State.DONE) for day in data[la])

            row.append(f"`{full:2}, {partial:2}`")

        rows.append(f"| `{year}` |{'|'.join(col.center(col_width+2) for col in row)}|")

    all_rows = "\n".join(rows)
    return f"{header}\n{divider}\n{all_rows}"


def set_progress(year: int, day: int, lang: Lang, state: State) -> None:
    """Set a puzzle day's completion state, then rebuild the year's and the repo's README tables."""
    # cogapp is a dev dependency, so only import it when needed; the `aoc` CLI imports this module
    from cogapp import Cog

    validate_puzzle_date(year, day)

    n_days = n_puzzle_days(year)
    filepath = BASE_DIR / f"{year}" / "README.md"
    data_table = parse_progress_json(filepath, n_days=n_days)

    data_table[lang][day - 1] = state

    with filepath.open("w") as f:
        f.write(f"<!-- {json.dumps(data_table)} -->\n")
        f.write(f"{HEADER}\n\n")
        f.write(f"{build_table(data_table, n_days=n_days)}\n")
    print(f"Puzzle status updated: ({year}, {day}, {lang}, {state.name.lower()})")

    # Update the base README with the new status using Cog & a dummy sys.argv
    cog = Cog()
    cog.main(["", "-r", str((BASE_DIR / "README.md").resolve())])
