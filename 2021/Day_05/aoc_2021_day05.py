import re
import typing as t
from collections import defaultdict
from pathlib import Path

COORDINATE = tuple[int, int]
LINE_EXP = r"(\d+),(\d+) -> (\d+),(\d+)"


def parse_vent_lines(
    raw_report: list[str],
) -> t.Generator[tuple[COORDINATE, COORDINATE], None, None]:
    """
    Parse the provided list of vent line definitions & yield endpoint coordinate pairs.

    Lines are assumed to be of the form `"x1,y1 -> x2,y2"`. All coordinates are assumed to be
    positive.
    """
    for line in raw_report:
        x1, y1, x2, y2 = (int(num) for num in re.findall(LINE_EXP, line)[0])
        yield (x1, y1), (x2, y2)


def _calc_step(start: int, end: int) -> t.Literal[-1, 0, 1]:
    """Calculate the iteration step `[-1, 0, 1]` for line coordinate iteration."""
    if end == start:
        return 0

    if (end - start) > 0:
        return 1
    else:
        return -1


def find_overlaps(raw_report: list[str], ignore_diag: bool = True) -> int:
    """
    Sum the number of coordinates that lie along at least two vent lines.

    If the `ignore_diag` flag is set, only horizontal and vertical vent lines are considered.
    """
    coordinate_grid: dict[COORDINATE, int] = defaultdict(int)
    for (x1, y1), (x2, y2) in parse_vent_lines(raw_report):
        dx = _calc_step(x1, x2)
        dy = _calc_step(y1, y2)
        if ignore_diag:
            if dx and dy:
                continue

        coordinate_grid[(x1, y1)] += 1
        while (x1, y1) != (x2, y2):
            x1 += dx
            y1 += dy
            coordinate_grid[(x1, y1)] += 1

    return sum(1 for val in coordinate_grid.values() if val >= 2)


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().splitlines()

    print(f"Part One: {find_overlaps(puzzle_input)}")
    print(f"Part Two: {find_overlaps(puzzle_input, ignore_diag=False)}")
