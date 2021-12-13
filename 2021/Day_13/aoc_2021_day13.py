import re
import typing as t
from pathlib import Path

FOLD_RE = re.compile(r"fold along (\w)=(\d+)")

COORD = tuple[int, int]


class Fold(t.NamedTuple):  # noqa: D101
    axis: str
    location: int


def parse_instructions(raw_instructions: str) -> tuple[set[COORD], list[Fold]]:
    """
    Parse the provided instruction manual information into its dot coordinate & folding directions.

    Raw instructions are assumed to be a series of one or more `x,y` coordinate pairs, delimited by
    newlines. After the final coordinate, a blank line is expected, followed by one or more folding
    instructions of the form `"fold along <axis>=<location>"`, where axis is expected to be either
    `"x"` or `"y"` and location is an integer value along the axis.
    """
    coordinates, folds = raw_instructions.split("\n\n")
    parsed_coordinates = set()
    for line in coordinates.splitlines():
        x, y = line.split(",")
        parsed_coordinates.add((int(x), int(y)))

    parsed_folds = []
    for fold in folds.splitlines():
        axis, location = FOLD_RE.findall(fold)[0]
        parsed_folds.append(Fold(axis.lower(), int(location)))

    return parsed_coordinates, parsed_folds


def fold_paper(coords: set[COORD], folds: list[Fold]) -> set[COORD]:
    """
    Run through the provided folding instructions & update the set of initial dot coordinates.

    NOTE: It is assumed that no folding axis will be located along a line where dots are present.
    """
    for fold in folds:
        # When we fold across an axis, we can calculate the updated coordinates with some simple
        # arithmetic
        # e.g. for a fold across the y axis at y = 2, we want:
        #     0           0
        #     1           1
        #     - to become -
        #     3           1
        #     4           0
        #
        # Which we get from (fold - (coord - fold))
        if fold.axis == "x":
            coords = {
                (x if (x < fold.location) else (fold.location - (x - fold.location)), y)
                for x, y in coords
            }
        elif fold.axis == "y":
            coords = {
                (x, y if (y < fold.location) else (fold.location - (y - fold.location)))
                for x, y in coords
            }

    return coords


def _find_max(coords: set[COORD]) -> tuple[int, int]:
    """Find the maximum x & y values in the provided set of coordinates."""
    max_x = 0
    max_y = 0
    for x, y in coords:
        if x > max_x:
            max_x = x

        if y > max_y:
            max_y = y

    return max_x, max_y


def prettyprint(coords: set[COORD]) -> str:
    """Prettyprint the provided `(x,y)` coordinates so we can decipher the instructions."""
    n_cols, n_rows = _find_max(coords)
    rows = []
    for y in range(n_rows + 1):
        rows.append("".join("#" if (x, y) in coords else " " for x in range(n_cols + 1)))

    return "\n".join(rows)


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text()
    dot_coords, folds = parse_instructions(puzzle_input)

    print(f"Part One: {len(fold_paper(dot_coords, [folds[0]]))}")
    print(f"Part Two:\n{prettyprint(fold_paper(dot_coords, folds))}")
