from __future__ import annotations

from collections import abc
from dataclasses import dataclass
from enum import Enum
from functools import partial
from pathlib import Path

from helpers.geometry import BoundingBox, COORD


class TiltDirection(Enum):  # noqa: D101
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


SPIN_CYCLE = (TiltDirection.NORTH, TiltDirection.WEST, TiltDirection.SOUTH, TiltDirection.EAST)


DELTA_MAP = {
    TiltDirection.NORTH: (0, -1, partial(sorted, key=lambda r: r[1])),
    TiltDirection.EAST: (1, 0, partial(sorted, key=lambda r: r[0], reverse=True)),
    TiltDirection.SOUTH: (0, 1, partial(sorted, key=lambda r: r[1], reverse=True)),
    TiltDirection.WEST: (-1, 0, partial(sorted, key=lambda r: r[0])),
}


@dataclass
class PlatformMap:  # noqa: D101
    rocks: set[COORD]
    cube_rocks: set[COORD]
    bbox: BoundingBox

    def _render_map(self) -> str:
        rows = []
        for y in self.bbox.y_bound:
            cols = []
            for x in self.bbox.x_bound:
                if (x, y) in self.rocks:
                    cols.append("O")
                elif (x, y) in self.cube_rocks:
                    cols.append("#")
                else:
                    cols.append(".")

            rows.append("".join(cols))

        return "\n".join(rows)

    @property
    def support_load(self) -> int:
        """
        Calculate the total load on the north support beam.

        The amount of load on the beam caused by a single tock is equal to the number of rows from
        the rock to the south edge of the platform, including the row the rock is on. Cube-shaped
        rocks do not contribute to the beam's load.
        """
        most_south = self.bbox.y_bound[-1]
        return sum((most_south - y + 1) for _, y in self.rocks)

    def tilt(self, direction: TiltDirection) -> None:
        """
        Tilt the platform in the specified direction & allow all rocks to roll.

        Rocks will roll in a direction if there is an empty space for it to roll into; cube-shaped
        rocks will not roll. Rocks cannot roll off the edge of the platform.
        """
        dx, dy, sorter = DELTA_MAP[direction]

        # Sorter arranges the rocks for iteration based on the relevant coordinate for the current
        # tilt direction. e.g. for a North tilt we want to work from the top down
        rock_order = sorter(self.rocks)
        new_pos = set()
        for coord in rock_order:
            start_x, start_y = coord
            while True:
                qc = (start_x + dx, start_y + dy)
                if any(
                    (
                        (qc in new_pos),  # Other rocks
                        (qc in self.cube_rocks),  # Cube rocks are immobile
                        (qc not in self.bbox),  # Can't roll off
                    )
                ):
                    # Can't roll further
                    new_pos.add((start_x, start_y))
                    break

                start_x, start_y = qc

        self.rocks = new_pos

    def spin_cycle(
        self, n_cycles: int = 1_000_000_000, cycle_spec: abc.Iterable[TiltDirection] = SPIN_CYCLE
    ) -> None:
        """Run through n cycles of the platform's spin cycle."""
        # Track the rock positions and the cycle iteration they were last seen
        seen: dict[frozenset[COORD], int] = {}

        n = 0
        while True:
            if n == n_cycles:
                return

            # Short circuit if we've come across a rock state that we've already seen before
            pre = frozenset(self.rocks)
            if pre in seen:
                break
            else:
                seen[pre] = n

            for direction in cycle_spec:
                self.tilt(direction)

            n += 1

        # If we're here, we've found a cycle in the...cycles
        cycle_length = n - seen[pre]
        n_remaining = (n_cycles - n) % cycle_length

        for _ in range(n_remaining):
            for direction in cycle_spec:
                self.tilt(direction)

    @classmethod
    def from_raw(cls, raw_map: str) -> PlatformMap:
        """
        Parse the provided platform map.

        The map is provided as a series of lines of legend characters, `O` represents the location
        of a round rock, `#` represents the location of a cube shaped rock, and `.` denotes an empty
        space.
        """
        rocks = set()
        cube_rocks = set()
        for y, row in enumerate(raw_map.splitlines()):
            for x, c in enumerate(row):
                if c == "O":
                    rocks.add((x, y))
                elif c == "#":
                    cube_rocks.add((x, y))

        bbox = BoundingBox(((0, 0), (x, y)))  # Capture the platform's edges
        return cls(rocks, cube_rocks, bbox)


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    pmap = PlatformMap.from_raw(puzzle_input)
    pmap.tilt(TiltDirection.NORTH)
    print(f"Part One: {pmap.support_load}")

    pmap = PlatformMap.from_raw(puzzle_input)
    pmap.spin_cycle()
    print(f"Part Two: {pmap.support_load}")
