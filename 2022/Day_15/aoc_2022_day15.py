from __future__ import annotations

import re
import typing as t
from dataclasses import dataclass, field
from pathlib import Path

COORD: t.TypeAlias = tuple[int, int]

REPORT_LOC = re.compile(r"[xy]=(-?\d+)")


def parse_sensor_map(raw_report: str) -> t.Iterable[tuple[COORD, COORD]]:
    """"""
    for report in raw_report.splitlines():
        s_x, s_y, b_x, b_y = (int(val) for val in REPORT_LOC.findall(report))
        yield (s_x, s_y), (b_x, b_y)


def manhattan_dist(origin: COORD, destination: COORD) -> int:  # noqa: D103
    return abs(origin[0] - destination[0]) + abs(origin[1] - destination[1])


@dataclass
class SensorField:  # noqa: D101
    origin: COORD
    radius: int

    _x_extent: range = field(init=False, repr=False)
    _y_extent: range = field(init=False, repr=False)

    def __post_init__(self) -> None:
        x, y = self.origin
        self._x_extent = range(x - self.radius, x + self.radius + 1)
        self._y_extent = range(y - self.radius, y + self.radius + 1)

    def __contains__(self, query: COORD) -> bool:
        x, y = query
        # Start with the easy absolute bounds on each axis
        if (x not in self._x_extent) or (y not in self._y_extent):
            return False

        # Since the field is a diamond, we know how its shape changes with each step away from the
        # origin
        # Steps are symmetric in each direction so we can just use absolute value to make math easy
        dx = abs(x - self.origin[0])
        dy = abs(y - self.origin[1])
        x_width = self.radius - dy
        y_width = self.radius - dx
        layer_x_extent = range(self.origin[0] - x_width, self.origin[0] + x_width + 1)
        layer_y_extent = range(self.origin[1] - y_width, self.origin[1] + y_width + 1)

        return x in layer_x_extent and y in layer_y_extent

    @classmethod
    def cluster_from_sensor_map(cls, raw_report: str) -> list[SensorField]:  # noqa: D102
        readings = parse_sensor_map(raw_report)
        return [cls(sensor, manhattan_dist(sensor, beacon)) for sensor, beacon in readings]


def n_nonbeacon_1d(
    sensor_field: t.Iterable[SensorField], beacons: set[COORD], query_y: int = 2_000_000
) -> int:
    # Since we know the ranges of all the sensors, we can determine the range of x values we need to
    # check
    # Since we're only at one elevation we just have to do this for the x values
    lbound = min(min(s._x_extent) for s in sensor_field)
    ubound = max(max(s._x_extent) for s in sensor_field) + 1

    n_covered = 0
    for x in range(lbound, ubound):
        coord = (x, query_y)
        for s_field in sensor_field:
            if coord in s_field and coord not in beacons:
                n_covered += 1
                break

    return n_covered


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text()

    # Can be smarter and not parse twice but it's not important enough
    fields = SensorField.cluster_from_sensor_map(puzzle_input)
    beacons = set(thing for _, thing in parse_sensor_map(puzzle_input))

    print(f"Part One: {n_nonbeacon_1d(fields, beacons, 2_000_000)}")
    print(f"Part Two: {...}")
