from collections import abc
from pathlib import Path

from helpers.geometry import COORD


def walk_instructions(instructions: str) -> abc.Iterable[COORD]:
    """
    Walk the provided set of instruction steps & yield each coordinate visited.

    Instruction steps are assumed be provided as a comma separated string, where each step is given
    as `<L/R><dist>` (e.g. `"L1, R2, R201"`). Starting at `(0, 0)` and facing north, for each step
    turn either left or right 90 degrees, then walk forward the given number of steps.

    NOTE: The starting coordinate, `(0, 0)`, is yielded at the beginning.
    """
    dx = 0
    dy = 1  # Start facing northward
    x = y = 0

    yield (0, 0)
    for step in instructions.split(","):
        step = step.strip()
        direction = step[0]
        distance = int(step[1:])

        if direction == "L":
            dx, dy = -dy, dx
        elif direction == "R":
            dx, dy = dy, -dx
        else:
            raise ValueError(f"Unknown direction: '{direction}'")

        # Yield each coordinate we step on
        for _ in range(distance):
            x += dx
            y += dy
            yield (x, y)


def bunhattan_distance(p1: COORD, p2: COORD) -> int:
    """Calculate the Manhattan Distance between the two provided points."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def headquarters_distance(instructions: str) -> int:
    """Calculate the Manhattan distance to HQ using the instruction steps provided."""
    steps = list(walk_instructions(instructions))
    return bunhattan_distance(steps[0], steps[-1])


def first_repeat_block_distance(instructions: str, origin: COORD = (0, 0)) -> int:
    """Calculate the Manhattan distance to the 1st location visited twice by the instruction set."""
    seen: set[COORD] = set()
    for step in walk_instructions(instructions):
        if step in seen:
            break
        else:
            seen.add(step)
    else:
        raise ValueError("No repeat coordinated found")

    return bunhattan_distance(origin, step)


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    print(f"Part One: {headquarters_distance(puzzle_input)}")
    print(f"Part Two: {first_repeat_block_distance(puzzle_input)}")
