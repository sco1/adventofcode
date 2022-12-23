from __future__ import annotations

import re
import typing as t
from enum import IntEnum
from pathlib import Path

COORD: t.TypeAlias = tuple[int, int]
COORDS: t.TypeAlias = set[COORD]

INSTRUCTION_RE = re.compile(r"(\d+)([RL])?")


class Rotate(IntEnum):  # noqa: D101
    CW = 1
    CCW = -1


class Facing(IntEnum):  # noqa: D101
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


DELTAS = {
    Facing.RIGHT: (1, 0),
    Facing.DOWN: (0, 1),
    Facing.LEFT: (-1, 0),
    Facing.UP: (0, -1),
}


class Instruction(t.NamedTuple):  # noqa: D101
    n_steps: int
    then_rotate: Rotate | None

    @classmethod
    def from_raw_tuple(cls, raw: tuple[str, str]) -> Instruction:  # noqa: D102
        raw_n, raw_dir = raw
        if not raw_dir:
            direction = None
        elif raw_dir == "R":
            direction = Rotate.CW
        elif raw_dir == "L":
            direction = Rotate.CCW
        else:
            raise ValueError(f"Unknown rotation direction: '{raw_dir}'")

        return cls(int(raw_n), direction)


INSTRUCTIONS: t.TypeAlias = t.Iterable[Instruction]
BOUNDS: t.TypeAlias = tuple[list[range], list[range]]


def _parse_map(raw_map: str) -> tuple[COORDS, COORDS, BOUNDS]:
    """
    Parse the provided map into its open floor and wall coordinates.

    Coordinate bounds for each layer are also provided in each direction.

    Open floor spaces are assumed to be denoted by `"."` and walls denoted by `"#"`.
    """
    floor = set()
    walls = set()
    x_bounds = []
    for y, line in enumerate(raw_map.splitlines()):
        x_min = x_max = None
        for x, glyph in enumerate(line):
            if glyph == ".":
                floor.add((x, y))
            elif glyph == "#":
                walls.add((x, y))
            else:
                continue

            if x_min is None:
                x_min = x

            if (x_max is None) or (x > x_max):
                x_max = x

        if (x_min is None) or (x_max is None):
            raise ValueError(f"Could not locate x bounds at layer {y}")

        x_bounds.append(range(x_min, x_max + 1))

    # Can probably do some fancy thing to get the y bounds at the same time, but this is fine
    # I'm going to assume that there's at least one valid floor tile with x=0 & that the map doesn't
    # have any islands
    y_bounds = []
    max_x = max(max(bound) for bound in x_bounds)
    joined = floor | walls
    for i_x in range(max_x + 1):
        y_min = min(y for x, y in joined if x == i_x)
        y_max = max(y for x, y in joined if x == i_x)

        y_bounds.append(range(y_min, y_max + 1))

    return floor, walls, (x_bounds, y_bounds)


def _parse_instructions(raw_instructions: str) -> INSTRUCTIONS:
    """
    Parse the provided instructions and split each into their components.

    Raw instructions are assumed to be of the form e.g. `10R5L5R10L4R5L5`, where a new instruction
    is assumed to begin with each number. The number indicates the number of tiles to move and the
    letter indicates the turn direction after movement stops. The final instruction is assumed to
    have no turn direction.
    """
    matches = INSTRUCTION_RE.findall(raw_instructions)
    if not matches:
        raise ValueError("Could not parse provided instruction string.")

    for match in matches:
        yield Instruction.from_raw_tuple(match)


def parse_puzzle_input(  # noqa: D103
    puzzle_input: str,
) -> tuple[COORDS, COORDS, BOUNDS, INSTRUCTIONS]:
    raw_map, raw_instructions = puzzle_input.split("\n\n")
    floor, walls, bounds = _parse_map(raw_map)
    instructions = _parse_instructions(raw_instructions)

    return floor, walls, bounds, instructions


def _wrap_in_range(val: int, bounds: range) -> int:
    """Shift the query val so its wrapped into the provided bounding range."""
    return ((val - min(bounds)) % len(bounds)) + min(bounds)


def _peek(start: COORD, direction: Facing, bounds: tuple[list[range], list[range]]) -> COORD:
    """Return a coordinate shifted in the provided direction, wrapping around the edge if needed."""
    x, y = start
    dx, dy = DELTAS[direction]
    x_bounds, y_bounds = bounds

    x_n = _wrap_in_range((x + dx), x_bounds[y])
    y_n = _wrap_in_range((y + dy), y_bounds[x])

    return (x_n, y_n)


def find_password(floor: COORDS, walls: COORDS, bounds: BOUNDS, instructions: INSTRUCTIONS) -> int:
    """
    Traverse the path through the grove as described by the provided instructions.

    For each instruction, you move the number of steps described or until you encounter a wall. If
    an instruction would take you off the map, you wrap around to the other side of the board; there
    may be a wall in this position. Once you are unable to move any further, you rotate as
    instructed to face a new direction and move to the next instruction.

    Once instructions have been exhasted, the password can be calculated by summing 1000 times the
    row, 4 times the column, and the final facing direction. Facing is enumerated as: `0` for right,
    `1` for down, `2` for left, and `3` for up.
    """
    loc = (min(bounds[0][0]), 0)
    facing = Facing.RIGHT
    for instruction in instructions:
        for _ in range(instruction.n_steps):
            next_loc = _peek(loc, facing, bounds)

            # Check for wall
            if next_loc in walls:
                break

            # Otherwise move
            loc = next_loc

        if instruction.then_rotate is not None:
            facing = Facing((facing + instruction.then_rotate) % 4)

    col_f, row_f = loc
    return (1000 * (row_f + 1)) + (4 * (col_f + 1)) + facing  # Calculation assumes 1-indexed


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text()

    floor, walls, bounds, instructions = parse_puzzle_input(puzzle_input)
    print(f"Part One: {find_password(floor, walls, bounds, instructions)}")
    print(f"Part Two: {...}")
