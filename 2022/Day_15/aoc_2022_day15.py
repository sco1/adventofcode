from __future__ import annotations

import itertools
import re
import typing as t
from dataclasses import dataclass, field
from pathlib import Path

COORD: t.TypeAlias = tuple[int, int]

REPORT_LOC = re.compile(r"[xy]=(-?\d+)")


def parse_sensor_map(raw_report: str) -> t.Iterable[tuple[COORD, COORD]]:
    """
    Parse the provided sensor report and yield Sensor,Beacon coordinate tuples.

    Sensor reports are assumed to be newline delimited and of the form e.g.:
    `Sensor at x=2, y=18: closest beacon is at x=-2, y=15`, which would yield `((2, 18), (-2, 15))`
    """
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

    # Line equation intercepts for Part 2
    _a_int: tuple[int, int] = field(init=False, repr=False)  # Slope is 1
    _b_int: tuple[int, int] = field(init=False, repr=False)  # Slope is -1

    def __post_init__(self) -> None:
        x, y = self.origin
        self._x_extent = range(x - self.radius, x + self.radius + 1)
        self._y_extent = range(y - self.radius, y + self.radius + 1)

        # Line equation intercepts for just outside the field boundary
        self._a_int = (y - x + self.radius + 1, y - x - self.radius - 1)  # Slope is 1
        self._b_int = (x + y + self.radius + 1, x + y - self.radius - 1)  # Slope is -1

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

        return (x in layer_x_extent) and (y in layer_y_extent)

    @classmethod
    def cluster_from_sensor_map(cls, raw_report: str) -> list[SensorField]:  # noqa: D102
        readings = parse_sensor_map(raw_report)
        return [cls(sensor, manhattan_dist(sensor, beacon)) for sensor, beacon in readings]


def n_nonbeacon_1d(
    sensor_field: t.Iterable[SensorField], beacons: set[COORD], query_y: int = 2_000_000
) -> int:
    """Calculate the number of positions at a given elevation that cannot contain a beacon."""
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


def _inclrange(lbound: int, ubound: int) -> range:  # noqa: D103
    return range(lbound, ubound + 1)


# Don't use this on the puzzle input lol
def identify_tuning_frequency_brute(  # noqa: D103
    sensor_field: t.Iterable[SensorField],
    beacons: set[COORD],
    x_bound: tuple[int, int] = (0, 4_000_000),
    y_bound: tuple[int, int] = (0, 4_000_000),
) -> int:
    for check_coord in itertools.product(_inclrange(*x_bound), _inclrange(*y_bound)):
        if check_coord in beacons:
            continue

        if not any(check_coord in field for field in sensor_field):
            break
    else:
        # If we're here, then we didn't find a location
        raise ValueError("Could not locate distress beacon in the given coordinate bounds.")

    x, y = check_coord
    tuning_frequency = (4_000_000 * x) + y
    return tuning_frequency


def identify_tuning_frequency(
    sensor_field: t.Iterable[SensorField],
    beacons: set[COORD],
    x_bound: tuple[int, int] = (0, 4_000_000),
    y_bound: tuple[int, int] = (0, 4_000_000),
) -> int:
    """
    Calculate the tuning frequency needed to isolate the distress beacon's signal.

    The distress beacon is assumed to be within the given (inclusive) x and y bounds, and there is
    assumed to be only one beacon in these bounds. The tuning frequency is calculated by multiplying
    this location's x coordinate by `4,000,000` and then adding its y coordinate.
    """
    x_r = _inclrange(*x_bound)
    y_r = _inclrange(*y_bound)
    # Since we're assuming there is only one valid location, the point must lie just outside the
    # field boundary of at least two sensors. This allows us to only have to consider points that
    # lie at these intersections & drastically shrink the query space
    for left, right in itertools.permutations(sensor_field, 2):
        # Use chain to stack the two sensors' coefficients
        a_ints = itertools.chain.from_iterable((left._a_int, right._a_int))
        b_ints = itertools.chain.from_iterable((left._b_int, right._b_int))
        for a, b in itertools.product(a_ints, b_ints):
            x_int, y_int = ((b - a) // 2, (a + b) // 2)  # Calculate intersection point
            if (x_int not in x_r) or (y_int not in y_r) or ((x_int, y_int) in beacons):
                continue

            if all((x_int, y_int) not in field for field in sensor_field):
                return 4_000_000 * x_int + y_int


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text()

    # Can be smarter and not parse twice but it's not important enough
    fields = SensorField.cluster_from_sensor_map(puzzle_input)
    beacons = {thing for _, thing in parse_sensor_map(puzzle_input)}

    print(f"Part One: {n_nonbeacon_1d(fields, beacons)}")
    print(f"Part Two: {identify_tuning_frequency(fields, beacons)}")
