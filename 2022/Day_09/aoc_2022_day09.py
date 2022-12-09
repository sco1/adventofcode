from __future__ import annotations

import typing as t
from pathlib import Path

STEP_DELTA = {
    "L": (-1, 0),
    "R": (1, 0),
    "U": (0, 1),
    "D": (0, -1),
}
ABS_ADJACENT = {(1, 0), (0, 1), (1, 1)}


class Instruction(t.NamedTuple):  # noqa: D101
    direction: str
    n_steps: int

    @classmethod
    def from_raw(cls, raw_instruction: str) -> Instruction:
        """
        Parse instructions from a line of the puzzle input.

        Expected to be of the form e.g. `"R 5"` or `"U 8"`
        """
        direction, n_steps = raw_instruction.strip().split()
        return cls(direction, int(n_steps))


def parse_instructions(puzzle_input: str) -> t.Generator[Instruction, None, None]:  # noqa: D103
    return (Instruction.from_raw(line) for line in puzzle_input.splitlines())


def _step_toward_adjacent(val: int) -> int:
    """Step the provided value towards 0 if `abs(val) > 1`, otherwise make no change."""
    if val > 1:
        return val - 1
    elif val < -1:
        return val + 1
    else:
        return val


def run_sim(instructions: t.Iterator[Instruction], n_knots: int = 2) -> int:
    """
    Step through the provided rope physics simulation and calculate the unique tail spaces seen.

    `n_knots` is assumed to be a positive integer greater than 2.

    For each time step, the head of the rope is moved in the described direction. Since the rope is
    quite short, each knot will always be touching the knot leading it. In terms of the grid, if the
    trailing knot is ever two steps directly up, down, left, or right from the leading knot, the
    trailing knot must also move one step in that direction so it remains close enough. Otherwise,
    if the head and tail aren't touching and aren't in the same row or column, the tail always moves
    one step diagonally to keep up.
    """
    rope = [(0, 0)] * n_knots
    knot_seen = [set([knot]) for knot in rope]

    for step_t in instructions:
        dx, dy = STEP_DELTA[step_t.direction]
        for _ in range(step_t.n_steps):
            # Move the head of the rope first
            h_x, h_y = rope[0]
            h_x += dx
            h_y += dy
            rope[0] = (h_x, h_y)

            for knot_idx, (k_x, k_y) in enumerate(rope[1:], start=1):
                ahead_x, ahead_y = rope[knot_idx - 1]
                if (k_x, k_y) == (ahead_x, ahead_y):  # Overlapping, tail doesn't move
                    continue

                k_dx = ahead_x - k_x
                k_dy = ahead_y - k_y
                if (abs(k_dx), abs(k_dy)) in ABS_ADJACENT:  # Tail is already touching, doesn't move
                    continue
                else:
                    k_x += _step_toward_adjacent(k_dx)
                    k_y += _step_toward_adjacent(k_dy)

                    rope[knot_idx] = (k_x, k_y)
                    knot_seen[knot_idx].add((k_x, k_y))

    return len(knot_seen[-1])


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text()

    print(f"Part One: {run_sim(parse_instructions(puzzle_input), 2)}")
    print(f"Part Two: {run_sim(parse_instructions(puzzle_input), 10)}")
