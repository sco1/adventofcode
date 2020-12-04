from __future__ import annotations

import math
from pathlib import Path


class TobogganMap:
    """Represent the toboggan slope mapped by the provided puzzle input."""

    _width: int  # Though it repeats, store the base width for wrapping indices
    _height: int

    def __init__(self, base_map: str):
        self.tree_map, dims = self.parse_map(base_map)
        self._width, self._height = dims

    def toboggan_run(self, start: tuple[int, int] = (0, 0), step: tuple[int, int] = (3, 1)) -> int:
        """Simulate a toboggan run from the provided start coordinates."""
        x_pos, y_pos = start
        n_collisions = 0
        while y_pos <= self._height:
            if (x_pos % self._width, y_pos) in self.tree_map:
                n_collisions += 1

            x_pos += step[0]
            y_pos += step[1]

        return n_collisions

    def check_step_sequence(self, step_sequence: list[tuple[int, int]]) -> int:
        """Check a sequence of simulation steps & return the product of their trees encountered."""
        trees_encountered = [self.toboggan_run(step=step_size) for step_size in step_sequence]
        return math.prod(trees_encountered)

    @staticmethod
    def parse_map(raw_map: str) -> tuple[set[tuple[int, int]], tuple[int, int]]:
        """
        Parse the provided map into a set of 0-indexed (x,y) tree location coordinates.

        Each line of the map is assumed to use `.` for open squares and `#` for trees.

        The origin is defined as the top left corner, with the positive X direction to the right and
        the positive Y direction dowards.

        A (width, height) tuple is also returned
        """
        tree_coordinates = set()
        for y, row in enumerate(raw_map.splitlines()):
            for x, symbol in enumerate(row):
                if symbol == "#":
                    tree_coordinates.add((x, y))

        return tree_coordinates, (x + 1, y)  # Add 1 to width since enumerate starts at 0


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text()

    run = TobogganMap(puzzle_input)
    print(f"Part 1: {run.toboggan_run(step=(3, 1))} trees hit")

    steps_sequence = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    print(f"Part 2: {run.check_step_sequence(steps_sequence)} tree encounter product")
