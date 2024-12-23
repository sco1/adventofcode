from __future__ import annotations

import math
import re
from collections import defaultdict, deque
from dataclasses import dataclass, field
from pathlib import Path

from helpers.geometry import BoundingBox, COORD


@dataclass(slots=True)
class Robot:  # noqa: D101
    position: COORD
    velocity: tuple[int, int]

    @classmethod
    def from_raw(cls, raw_params: str) -> Robot:
        """
        Build a `Robot` instance from the provided raw parameters.

        Parameters are assumed to be provided in the following form: `p=x,y v=dx,dy`, where `x`,
        `y`, `dx`, and `dy` are integers.
        """
        raw_comps = re.findall(r"(-?\d+)", raw_params)
        if not raw_comps:
            raise ValueError(f"Could not locate components in parameter string: {raw_params}")

        if len(raw_comps) != 4:
            raise ValueError(
                f"Could not locate all components in parameter string. Found: {len(raw_comps)}, expected: 4"  # noqa: E501
            )

        comps = [int(n) for n in raw_comps]
        x, y, dx, dy = comps

        return Robot(position=(x, y), velocity=(dx, dy))


@dataclass(slots=True)
class RobotGrid:  # noqa: D101
    width: int
    height: int
    robots: list[Robot]
    _bbox: BoundingBox = field(init=False)
    _quadrants: tuple[BoundingBox, BoundingBox, BoundingBox, BoundingBox] = field(init=False)

    def __post_init__(self) -> None:
        """
        Build the grid bounding box & quadrants from the provided grid dimensions.

        Quadrants are defined starting at the top left & continuing clockwise, e.g.:

        ```
           |
         0 | 1
        ___|___
           |
         3 | 2
           |
        ```

        NOTE: Both the horizontal and vertical middle coordinates are ignored when defining the grid
        quadrants; e.g. a grid of width `11` and height `7` does not include the lines defined by
        `x=5` and `y=3`.
        """
        self._bbox = BoundingBox.from_dims(width=self.width, height=self.height)

        w, h = self.width, self.height
        mid_horiz = w // 2
        mid_vert = h // 2

        # fmt: off
        quad_bounds = (
            ((0, 0), (mid_horiz-1, 0), (0, mid_vert-1), (mid_horiz-1, mid_vert-1)),
            ((mid_horiz+1, 0), (w-1, 0), (mid_horiz+1, mid_vert-1), (w-1, mid_vert-1)),
            ((mid_horiz+1, mid_vert+1), (w-1, mid_vert+1), (mid_horiz+1, h-1), (w-1, h-1)),
            ((0, mid_vert+1), (mid_horiz-1, mid_vert+1), (0, h-1), (mid_horiz-1, h-1)),
        )
        # fmt: on

        self._quadrants = tuple(BoundingBox(b) for b in quad_bounds)  # type: ignore[assignment]

    def step(self, n: int = 1) -> None:
        """
        Execute `n` steps of robot movement within the described grid.

        For each time step, each robot is moved in a straight line from its current position using
        its velocity. If a robot reaches the edge of the grid, it teleports (i.e. wraps) to the
        other side of the grid before continuing its movement.
        """
        for r in self.robots:
            vx, vy = r.velocity
            dx, dy = n * vx, n * vy
            r.position = self._bbox.wrap_shift(start=r.position, dx=dx, dy=dy)

    def cluster_robots(self) -> dict[COORD, int]:
        """
        Generate a coordinate -> number of robots mapping for all robots in the grid.

        NOTE: A coordinate location is only present in the calculated mapping if there is at least
        one robot present at that location.
        """
        cluster: dict[COORD, int] = defaultdict(int)
        for r in self.robots:
            cluster[r.position] += 1

        return cluster

    def render_grid(self) -> str:
        """
        Render the current grid & display the number of robots at each location.

        Empty grid locations are denoted by `.`.
        """
        cluster = self.cluster_robots()
        rows = []
        for y in self._bbox.y_bound:
            cols = []
            for x in self._bbox.x_bound:
                if (x, y) in cluster:
                    cols.append(f"{cluster[(x, y)]}")
                else:
                    cols.append(".")

            rows.append("".join(cols))

        return "\n".join(rows)

    def calculate_safety_factor(self) -> int:
        """
        Calculate the current safety factor of the grid.

        The safety factor is defined as the product of the robot counts in each grid quadrant; any
        robot that lies exactly in the middle of the grid (horizontally or vertically) do not count
        as being in any quadrant & are ignored by the calculation.
        """
        r_queue = deque(self.robots)
        quad_counts: dict[int, int] = defaultdict(int)
        while r_queue:
            r = r_queue.popleft()
            for i, q in enumerate(self._quadrants):
                if r.position in q:
                    quad_counts[i] += 1
                    break

        return math.prod(quad_counts.values())

    def find_tree(self) -> int:
        """
        Determine the fewest number of seconds that must elapse for an easter egg to be formed.

        Due to their programming, after a certain amount of time the robots should arrange
        themselves into a picture of a Christmas tree!
        """
        # There's likely an approach with cycle counting to notice when some alignment criteria are
        # met, but it seems like if we assume that the tree is only formed when no robots share a
        # location.
        # Might be a strong assumption but it appears to work and doesn't take an egregious amount
        # of time
        n_robots = len(self.robots)
        t = 0
        while True:
            self.step()
            t += 1

            n_locations = len(self.cluster_robots())
            if n_locations == n_robots:
                break

        return t


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    robots = [Robot.from_raw(ln) for ln in puzzle_input.splitlines()]

    grid = RobotGrid(width=101, height=103, robots=robots)
    grid.step(100)
    print(f"Part One: {grid.calculate_safety_factor()}")

    robots = [Robot.from_raw(ln) for ln in puzzle_input.splitlines()]
    grid = RobotGrid(width=101, height=103, robots=robots)
    print(f"Part Two: {grid.find_tree()}")
    print(grid.render_grid())
