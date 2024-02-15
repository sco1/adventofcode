import typing as t
from pathlib import Path

import more_itertools as miter


def is_possible_triangle(sides_spec: str) -> bool:
    """
    Determine if the provided side lengths form a valid triangle.

    A triangle is possible if the sum of two sides is always greater than the length of the third
    side.

    Sides are assumed to be given as a string of 3 space-delimited integer lengths.
    """
    sides = [int(s) for s in sides_spec.strip().split()]
    if len(sides) != 3:
        raise ValueError(f"Expected 3 sides, received: {len(sides)}")

    a, b, c = sides
    return all(
        (
            (a + b > c),
            (b + c > a),
            (c + a > b),
        )
    )


def parse_triangle_columns(full_spec: str) -> t.Iterable[str]:
    """
    Parse triangle specifications from the provided specification sheet.

    Triangle sides are assumed to be grouped by column, where each set of 3 numbers in the column
    specifies a triangle.

    NOTE: It is assumed that the number of rows is divisible by 3.
    """
    for line_group in miter.chunked(full_spec.strip().splitlines(), n=3, strict=True):
        chunk = []
        for line in line_group:
            chunk.append(line.split())

        for triangle in zip(*chunk):
            yield " ".join(triangle)


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text()

    print(f"Part One: {sum(is_possible_triangle(spec) for spec in puzzle_input.splitlines())}")

    vertical_spec = parse_triangle_columns(puzzle_input)
    print(f"Part Two: {sum(is_possible_triangle(spec) for spec in vertical_spec)}")
