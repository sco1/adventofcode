import typing as t
from pathlib import Path

COORD: t.TypeAlias = tuple[int, int, int]
CUBES: t.TypeAlias = set[COORD]


def parse_lava_scan(lava_scan: str) -> CUBES:
    """
    Parse the provided lava scan into a set of lava cube coordinates.

    Lava cube coordinates are assumed to be newline delimited `x,y,z` coordinate triples.
    """
    cubes = set()
    for cube in lava_scan.splitlines():
        cubes.add(tuple(int(val) for val in cube.split(",")))

    return cubes  # type: ignore[return-value]


def _iter_neighbors(origin: COORD) -> t.Iterable[COORD]:
    """Iterate over the non-diagonal 3D neighbors of the provided starting coordinate."""
    x, y, z = origin
    neighbors = (
        (x - 1, y, z),
        (x + 1, y, z),
        (x, y - 1, z),
        (x, y + 1, z),
        (x, y, z - 1),
        (x, y, z + 1),
    )

    for neighbor in neighbors:
        yield neighbor


def calc_surface_area(cubes: CUBES) -> int:
    """Calculate the exposed surface area of the provided cube map."""
    surface_area = 0
    for cube in cubes:
        surface_area += sum((neighbor not in cubes) for neighbor in _iter_neighbors(cube))

    return surface_area


def _get_bounds(cubes: CUBES) -> tuple[range, range, range]:
    """Generate a 1-width padded bounding cube around the provided set of coordinates."""
    bounds = []
    for dim in (0, 1, 2):
        lbound = min(cube[dim] for cube in cubes)
        rbound = max(cube[dim] for cube in cubes)

        # Include the max & pad the bounds by 1 in case there's a cube on the boundary
        bounds.append(range(lbound - 1, rbound + 2))

    return tuple(bounds)  # type: ignore[return-value]


def calc_exterior_surface_area(cubes: CUBES) -> int:
    """Calculate the exposed exterior surface area of the provided cube map."""
    # Build an outer boundary to stop the flood fill from going forever
    bounds = _get_bounds(cubes)

    # Start the fill from a cube just outside the lava
    air_start: COORD = tuple(min(dim) for dim in bounds)  # type: ignore[assignment]
    external_air = {air_start}
    fill_queue = [air_start]
    while fill_queue:
        check_cube = fill_queue.pop()

        # Do a bounds check first
        if any(
            (coord not in check_range)
            for coord, check_range in zip(check_cube, bounds, strict=True)
        ):
            continue

        new_empty = []
        for neighbor in _iter_neighbors(check_cube):
            if (neighbor in cubes) or (neighbor in external_air):
                continue

            new_empty.append(neighbor)

        external_air.update(new_empty)
        fill_queue.extend(new_empty)

    # Now check which lava faces border the external air
    surface_area = 0
    for cube in cubes:
        surface_area += sum(
            ((neighbor in external_air) and (neighbor not in cubes))
            for neighbor in _iter_neighbors(cube)
        )

    return surface_area


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text()

    cubes = parse_lava_scan(puzzle_input)
    print(f"Part One: {calc_surface_area(cubes)}")
    print(f"Part Two: {calc_exterior_surface_area(cubes)}")
