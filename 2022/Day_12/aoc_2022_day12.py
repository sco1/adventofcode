import typing as t
from pathlib import Path

import networkx as nx

from helpers.geometry import COORD, iter_neighbors

MAP: t.TypeAlias = dict[COORD, int]


def _char2height(char: str) -> int:  # noqa: D103
    return ord(char) - ord("a")


def parse_map(heightmap: str) -> tuple[MAP, COORD, COORD]:
    """
    Parse the given heightmap into an elevation mapping, along with the start and target locations.

    The elevation of each square of the grid is given by a single lowercase letter, where `a` is the
    lowest elevation, `b` is the next-lowest, and so on up to the highest elevation, `z`. Also
    included on the heightmap are marks for our current position (`S`), which has elevation `a`,
    and our target location (`E`), which has elevation `z`.

    The coordinate origin is set to the upper left corner of the map, with positive axes going to
    the left and down.
    """
    elevation_map = {}
    start_pos: COORD | None = None
    target_pos: COORD | None = None
    for y, line in enumerate(heightmap.splitlines()):
        for x, char in enumerate(line):
            if char == "S":
                elevation_map[(x, y)] = _char2height("a")
                start_pos = (x, y)
            elif char == "E":
                elevation_map[(x, y)] = _char2height("z")
                target_pos = (x, y)
            else:
                elevation_map[(x, y)] = _char2height(char)

    if start_pos is None:
        raise ValueError("Could not locate the start position.")
    if target_pos is None:
        raise ValueError("Could not locate the target position.")

    return elevation_map, start_pos, target_pos


def build_valid_steps(elevation_map: MAP) -> nx.DiGraph:
    """
    Convert the provided elevation map into a digraph whose edges represent valid hiking steps.

    Steps can be made exactly one square up, down, left, or right; the elevation of the destination
    square can be at most one higher than the elevation of the current square.
    """
    edge_height = _char2height("~")  # Use a value higher than "z" to keep from leaping off the edge
    valid_steps = nx.DiGraph()
    for coord, height in elevation_map.items():
        for tx, ty in iter_neighbors(coord):
            if elevation_map.get((tx, ty), edge_height) <= (height + 1):
                valid_steps.add_edge(coord, (tx, ty))

    return valid_steps


def find_shortest_hike(elevation_map: MAP, valid_steps: nx.DiGraph, end_pos: COORD) -> int:
    """Find the shortest hike to the target position starting from any 0 elevation point."""
    start_points = (coord for coord, h in elevation_map.items() if h == 0)
    min_dist = 999_999_999
    for start in start_points:
        try:
            pathlen = nx.shortest_path_length(valid_steps, start, end_pos)
            if pathlen < min_dist:
                min_dist = pathlen
        except nx.NetworkXNoPath:
            # Skip the start point if no path exists
            continue

    return min_dist


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text()

    elevation, start_pos, end_pos = parse_map(puzzle_input)
    valid_steps = build_valid_steps(elevation)

    print(f"Part One: {nx.shortest_path_length(valid_steps, start_pos, end_pos)}")
    print(f"Part Two: {find_shortest_hike(elevation, valid_steps, end_pos)}")
