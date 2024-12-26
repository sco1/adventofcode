from pathlib import Path

import networkx as nx

from helpers.geometry import COORD, iter_neighbors
from helpers.parsing import parse_map_objects


def parse_racetrack(raw_map: str) -> tuple[nx.Graph, COORD, COORD, set[COORD]]:
    """
    Parse the provided Race Condition Festival racetrack map into its components.

    The racetrack map is assumed to be provided as an ASCII grid, where `.` represents an empty
    track tile, `#` represents a wall, `S` represents the start position, and `E` represents the end
    position; the start and end positions also count as empty track tiles.

    A graph representation of the track tiles is returned, along with the start and end positions
    and a collection of the wall coordinates.

    NOTE: It is assumed that the racetrack is completely enclosed by walls.
    """
    start: COORD | None = None
    end: COORD | None = None
    walls = set()
    racetrack = nx.Graph()
    for loc, c in parse_map_objects(raw_map, empty_tile=""):
        if c == "S":
            start = loc
        if c == "E":
            end = loc

        if c == "#":
            walls.add(loc)
        else:
            racetrack.add_node(loc)

    if start is None:
        raise ValueError("Could not identify start location")
    if end is None:
        raise ValueError("Could not identify end location")

    # Connect the open tiles
    # The racetrack is assumed to be fully enclosed by walls so we shouldn't need to do a bounds
    # check
    for tile in racetrack.nodes:
        for n in iter_neighbors(tile):
            if n in walls:
                continue

            racetrack.add_edge(tile, n)

    return racetrack, start, end, walls


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    print(f"Part One: {...}")
    print(f"Part Two: {...}")
