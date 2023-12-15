import itertools
from collections import abc
from dataclasses import dataclass
from pathlib import Path

from helpers.geometry import BoundingBox, COORD
from helpers.parsing import parse_hashed_map


@dataclass
class Pattern:  # noqa: D101
    rocks: set[COORD]
    bbox: BoundingBox


def parse_patterns(mirror_map: str) -> list[Pattern]:
    """
    Parse the provided map into its component reflection mapping(s).

    Patterns are assumed to be provided in newline-delimited chunks, where each pattern is composed
    of one or more lines of characters denoting the locations of either ash (`.`) or rock (`#`).
    Each pattern is defined by its rock locations and an overall bounding box for the pattern.
    """
    mirrors = [parse_hashed_map(chunk) for chunk in mirror_map.split("\n\n")]
    bboxes = [BoundingBox(m) for m in mirrors]
    return [Pattern(r, b) for r, b in zip(mirrors, bboxes)]


def _render_pattern(pattern: Pattern) -> str:
    rows = []
    for y in pattern.bbox.y_bound:
        cols = []
        for x in pattern.bbox.x_bound:
            if (x, y) in pattern.rocks:
                cols.append("#")
            else:
                cols.append(".")

        rows.append("".join(cols))

    return "\n".join(rows)


def reflect(pattern: Pattern, axis: int, loc: int) -> Pattern:
    """
    Reflect the provided pattern across the axis positioned immediately after the provided location.

    Specify `0` to reflect across the y-axis and `1` to reflect across the x-axis.
    """
    reflected = set(pattern.rocks)
    if axis == 0:
        # Reflect across column
        x_range = range(loc)
        query_coords = itertools.product(x_range, pattern.bbox.y_bound)
    elif axis == 1:
        # Reflect across row
        y_range = range(loc)
        query_coords = itertools.product(pattern.bbox.x_bound, y_range)
    else:
        raise ValueError(f"Invalid axis specified: {axis}")

    for coord in query_coords:
        dest = [*coord]
        d = loc - dest[axis]
        dest[axis] = dest[axis] + 2 * d - 1

        tdest: COORD = tuple(dest)  # type: ignore[assignment]
        if tdest not in pattern.bbox:
            continue

        if coord not in pattern.rocks:
            if tdest in reflected:
                # Make sure ash locations overwrite any rocks that are present at the destination
                reflected.remove(tdest)
        else:
            reflected.add(tdest)

    return Pattern(reflected, pattern.bbox)


def find_reflections(pattern: Pattern) -> tuple[list[int], list[int]]:
    """Identify reflection locations across the xy axes that replicate the provided pattern."""
    axis_map = {0: pattern.bbox.x_bound, 1: pattern.bbox.y_bound}
    valid_rocks = []
    for axis in (0, 1):
        valid = []
        for idx in range(1, axis_map[axis][-1] + 1):
            reflected = reflect(pattern, axis, idx)
            if reflected.rocks == pattern.rocks:
                valid.append(idx)

        valid_rocks.append(valid)

    return tuple(valid_rocks)  # type: ignore[return-value]


def summarize_patterns(patterns: abc.Iterable[Pattern]) -> int:
    """
    Provide a reflection summary hash of the provided collection of patterns.

    For each pattern, the location of a vertical or horizontal reflection point is calculated that
    yields the given reflection pattern. It is assumed that each pattern has one horizontal OR one
    vertical reflection.

    The reflection hash for a given collection of patterns is calculated by adding the number of
    columns to the left of each vertical reflection to 100 multiplied by the number of rows above
    each horizontal line of reflection. e.g. if a collection of patterns has 5 reflected vertical
    columns and 4 reflected horizontal rows its hash would be 405.
    """
    n_vertical = 0
    n_horizontal = 0
    for p in patterns:
        vert_col, horiz_col = find_reflections(p)
        if vert_col and horiz_col:
            raise ValueError(
                f"Found both horizontal and vertical reflectons. Vertical: {vert_col}, Horizontal: {horiz_col}"  # noqa: E501
            )

        n_vertical += sum(vert_col)
        n_horizontal += sum(horiz_col)

    return n_vertical + 100 * n_horizontal


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    patterns = parse_patterns(puzzle_input)
    print(f"Part One: {summarize_patterns(patterns)}")
    print(f"Part Two: {...}")
