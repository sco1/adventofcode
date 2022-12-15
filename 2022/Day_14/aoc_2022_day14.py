import itertools
import typing as t
from pathlib import Path

import more_itertools as miter

COORD: t.TypeAlias = tuple[int, int]

SAND_ORIGIN = (500, 0)


def _order_range(a: int, b: int) -> range:  # noqa: D103
    return range(min(a, b), max(a, b) + 1, 1)


def parse_rock_traces(cave_scan: str) -> tuple[set[COORD], int]:
    """
    Parse the provided cave scan into coordinates of the rock structures.

    Each line of the provided cave scan is assumed to contain inflection points of the rock
    structures, delimited by `->`. Line segments are assumed to only be horizontal or vertical.

    e.g. `498,4 -> 498,5 -> 496,5` maps to following: `{(496, 5), (497, 5), (498, 4), (498, 5)}`

    The coordinate origin is set to the upper left corner of the map, with positive axes going to
    the left and down.
    """
    rock_coords: set[COORD] = set()
    lowest_rock: int | None = None  # Track the lowest point so we can ID infinite falls later
    for line in cave_scan.splitlines():
        for start, end in miter.windowed(line.split("->"), 2):
            if not start or not end:
                raise ValueError("Unknown rock specification encountered.")

            x_i, y_i = (int(val) for val in start.strip().split(","))
            x_f, y_f = (int(val) for val in end.strip().split(","))

            # Since our y index starts at 0 and increases as we go down, we have to use max
            # I'm sure this won't confuse me later...
            low_point = max(y_i, y_f)
            if not lowest_rock or (low_point > lowest_rock):
                lowest_rock = low_point

            rock_coords.update(itertools.product(_order_range(x_i, x_f), _order_range(y_i, y_f)))

    if lowest_rock is None:
        raise ValueError("Could not locate lowest rock height")

    return rock_coords, lowest_rock


def iter_fall(x: int, y: int) -> t.Iterable[COORD]:
    """Iterate over the possible sand fall directions (down, down left, then down right)."""
    yield x, y + 1
    yield x - 1, y + 1
    yield x + 1, y + 1


def simulate_sand_fill(
    solid_coords: set[COORD], lowest_rock: int, sand_origin: COORD = SAND_ORIGIN
) -> int:
    """
    Simulate the falling sand and run until the scanned cave no longer retains any grains.

    Sand is assumed to enter the cave one unit at a time; a new unit of sand does not enter the cave
    until the previous grain comes to rest. A unit of sand always falls down one step if possible;
    fall direction is prioritized as follows:
        1. Down
        2. Diagonal left
        3. Diagonal right

    If all 3 directions are blocked, then the unit of sand comes to rest. At some point, the cave is
    assumed to reach a filling threshold, after which each new grain of sand is assumed to fall
    forever. Once this point is reached, the simulation ends and the number of sand grains present
    is returned.
    """
    n_grains = 1
    sand_coord = sand_origin
    while True:
        # Check for a free-falling sand grain, it will be lower than any of the rocks
        if sand_coord[1] > lowest_rock:
            return n_grains - 1  # Don't count the currently falling grain

        for coord in iter_fall(*sand_coord):
            if coord not in solid_coords:
                sand_coord = coord
                break
        else:
            # If we're here, we couldn't move any more
            # Add the grain to our solids and reset
            solid_coords.add(sand_coord)
            n_grains += 1
            sand_coord = sand_origin


def fill_until_blocked(
    solid_coords: set[COORD], lowest_rock: int, sand_origin: COORD = SAND_ORIGIN
) -> int:
    """
    Simulate the falling sand and run until the scanned cave no longer retains any grains.

    Sand is assumed to enter the cave one unit at a time; a new unit of sand does not enter the cave
    until the previous grain comes to rest. A unit of sand always falls down one step if possible;
    fall direction is prioritized as follows:
        1. Down
        2. Diagonal left
        3. Diagonal right

    If all 3 directions are blocked, then the unit of sand comes to rest.

    The floor of the cave is located 2 units below the lowest rock face; for the purposes of the
    simulation it is assumed to be an infinite horizontal rock segment. The simulation runs until
    the sand origin is plugged, at which point the simulation ends and the number of sand grains
    present is returned.
    """
    floor_y = lowest_rock + 2

    n_grains = 1
    sand_coord = sand_origin
    while True:
        for coord in iter_fall(*sand_coord):
            # If one of the 3 is the floor they'll all be the floor but I can't think of anything
            # more clever to avoid going through them all
            if coord[1] == floor_y:
                continue

            if coord not in solid_coords:
                sand_coord = coord
                break
        else:
            # If we're here, we couldn't move any more
            # If we're still at the origin, block it with this grain and exit
            if sand_coord == sand_origin:
                return n_grains

            # Otherwise, add the grain to our solids and reset
            solid_coords.add(sand_coord)
            n_grains += 1
            sand_coord = sand_origin


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text()

    rock_coords, lowest = parse_rock_traces(puzzle_input)
    print(f"Part One: {simulate_sand_fill(rock_coords, lowest)}")

    rock_coords, lowest = parse_rock_traces(puzzle_input)
    print(f"Part Two: {fill_until_blocked(rock_coords, lowest)}")
