from __future__ import annotations

from collections import abc
from dataclasses import dataclass
from pathlib import Path

from helpers.geometry import MoveDir

DIRECTION_MAP = {
    "U": MoveDir.NORTH,
    "3": MoveDir.NORTH,
    "R": MoveDir.EAST,
    "0": MoveDir.EAST,
    "D": MoveDir.SOUTH,
    "1": MoveDir.SOUTH,
    "L": MoveDir.WEST,
    "2": MoveDir.WEST,
}


@dataclass
class Instruction:  # noqa: D101
    direction: MoveDir
    n: int
    color: str

    @classmethod
    def from_color(cls, color: str) -> Instruction:
        """
        Translate the provided hexadecimal color string into its true instructions.

        The provided color string is assumed to be provided in the form: `#70c710` (with leading
        `#`). The first 5 digits of the number correspond to the dig distance, and the final digit
        corresponds to the dig direction: `0` means `R`, `1` means `D`, `2` means `L`, and `3`
        means `U`; e.g. the provided example maps to `R 461937`.
        """
        direction = DIRECTION_MAP.get(color[-1])
        if direction is None:
            raise ValueError(f"Unknown direction: '{color[-1]}'")

        n = int(f"0x{color[1:6]}", 0)
        return cls(direction, n, color)


def parse_dig_instructions(dig_instructions: str) -> list[Instruction]:
    """
    Parse the provided dig instructions into their respective `Instruction` instances.

    Instructions are assumed to be provided as a sequence of lines, where each line is of the form:
    <dig direction> <dig distance> (<color code>), e.g. `R 6 (#70c710)`.
    """
    instructions = []
    for line in dig_instructions.splitlines():
        raw_direction, raw_n, color = line.split()

        if raw_direction == "U":
            direction = MoveDir.NORTH
        elif raw_direction == "R":
            direction = MoveDir.EAST
        elif raw_direction == "D":
            direction = MoveDir.SOUTH
        elif raw_direction == "L":
            direction = MoveDir.WEST
        else:
            raise ValueError(f"Unknown direction: '{raw_direction}'")

        instructions.append(Instruction(direction, int(raw_n), color.strip("()")))

    return instructions


def dig_trench(
    dig_instructions: abc.Iterable[Instruction], fill: bool = True, translate_color: bool = False
) -> int:
    """
    Dig the trench according to the provided instructions and calculate the total dig volume.

    Starting at `(0, 0)`, for each step of the provided instructions a 1 meter cube hole is dug at
    each location along the line described by the instruction. The instructions are assumed to form
    the perimeter of a closed polygon. If `fill` is `True`, the interior of this polygon is also dug
    out.

    If `translate_color` is `True`, the dig instructions for each step are instead calculated from
    the instruction's hexidecimal color string. See: `Instruction.from_color` for the description of
    how to interpret this string.
    """
    curr = (0, 0)
    n_dug = 0
    vertices = [curr]
    for s in dig_instructions:
        if translate_color:
            s = Instruction.from_color(s.color)

        for _ in range(s.n):
            curr = s.direction.shift(curr)

        vertices.append(curr)
        n_dug += s.n

    # Use the shoelace formula to calculate the area of the polygon formed by the trench
    # https://en.wikipedia.org/wiki/Shoelace_formula
    # Thanks Gauss!
    if fill:
        # Iterate over the vertices we have, but append the starting point to wrap the final row
        n_vertices = len(vertices)
        vertices.append((0, 0))
        area = 0
        for i in range(n_vertices):
            vert, next_vert = vertices[i], vertices[i + 1]
            area += (vert[0] * next_vert[1]) - (vert[1] * next_vert[0])
        area = abs(area) // 2

        # Once we have the area, we need to accound for the boundary trench that's already been dug.
        # Since we've centered the holes at the coordinate locations, the calculated area already
        # accounts for half of the trench, so we have to add the other half. The +1 I'm still not
        # quite understanding, but it has something to do with accounting for the corners
        n_dug = area + n_dug // 2 + 1

    return n_dug


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    instructions = parse_dig_instructions(puzzle_input)
    print(f"Part One: {dig_trench(instructions)}")
    print(f"Part Two: {dig_trench(instructions, translate_color=True)}")
