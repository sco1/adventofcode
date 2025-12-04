from collections import abc

from helpers.geometry import COORD


def parse_map_objects(
    raw_map: str, x_start: int = 0, y_start: int = 0, empty_tile: str = "."
) -> abc.Iterator[tuple[COORD, str]]:
    """Parse the provided map and yield coordinate, value tuples for each non-empty tile."""
    for y, line in enumerate(raw_map.splitlines(), start=y_start):
        for x, c in enumerate(line, start=x_start):
            if c != empty_tile:
                yield ((x, y), c)


def parse_hashed_map(
    raw_map: str, marker: str = "#", x_start: int = 0, y_start: int = 0
) -> set[COORD]:
    """
    Parse the provided map into a set of coordinates for its marked points of interest.

    NOTE: The origin is assumed to be the top left corner of the map, with the y-axis facing
    downwards.
    """
    coords = set()
    for coord, c in parse_map_objects(raw_map, x_start, y_start):
        if c == marker:
            coords.add(coord)

    return coords
