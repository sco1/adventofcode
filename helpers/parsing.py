import typing as t

COORD: t.TypeAlias = tuple[int, int]


def parse_hashed_map(raw_map: str, x_start: int = 0, y_start: int = 0) -> set[COORD]:
    """
    Parse the provided map into a set of coordinates marking points of interest (`#`).

    NOTE: The origin is assumed to be the top left corner of the map, with the y-axis facing
    downwards.
    """
    coords = set()
    for y, line in enumerate(raw_map.splitlines(), start=y_start):
        for x, c in enumerate(line, start=x_start):
            if c == "#":
                coords.add((x, y))

    return coords
