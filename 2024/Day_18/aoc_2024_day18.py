from pathlib import Path

import networkx as nx

from helpers.geometry import BoundingBox, COORD, iter_neighbors


def parse_byte_positions(incoming_bytes: str) -> list[COORD]:
    """
    Parse the incoming byte locations coming down from the pushdown automaton.

    Byte positions are assumed to be a stream of newline-delimited `X,Y` integer coordinate pairs,
    e.g.:

    ```
    5,4
    4,2
    4,5
    3,0
    2,1
    ```
    """
    byte_positions = []
    for rb in incoming_bytes.splitlines():
        x, y = rb.split(",")
        byte_positions.append((int(x), int(y)))

    return byte_positions


def build_grid(byte_positions: list[COORD], dim: int, n_bytes: int) -> nx.Graph:
    """
    Build a graph representation of the memory grid that describes traversable spaces.

    As bytes fall into the memory grid, they make that coordinate corrupted and cannot be entered by
    entities traversing the grid. Entities also cannot leave the boundaries of the memory grid.
    """
    grid_bbox = BoundingBox.from_dims(width=dim, height=dim)
    corrupted_tiles = set(byte_positions[:n_bytes])
    grid = nx.Graph()

    for tile in grid_bbox.iter_points():
        if tile in corrupted_tiles:
            continue

        for n in iter_neighbors(tile):
            if (n not in grid_bbox) or (n in corrupted_tiles):
                continue

            grid.add_edge(tile, n)

    return grid


def shortest_path(grid: nx.Graph, start: COORD = (0, 0), end: COORD = (70, 70)) -> int:
    """Determine the minimum number of steps required to walk between the start and end tiles."""
    return nx.shortest_path_length(grid, source=start, target=end)


def find_first_blocker(
    byte_positions: list[COORD], dim: int, start: COORD = (0, 0), end: COORD = (70, 70)
) -> COORD:
    """Locate the coordinates of the first byte that prevent the exit from being reachable."""
    # A bit of brute force: just iterate through the bytes until we get a graph where there is no
    # path between the start and end nodes. It's a bit slow but it does eventually get there :)
    n_bytes = 0
    while True:
        grid = build_grid(byte_positions, dim=dim, n_bytes=n_bytes)
        if not nx.has_path(grid, source=start, target=end):
            return byte_positions[n_bytes - 1]

        n_bytes += 1


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    byte_positions = parse_byte_positions(puzzle_input)

    grid = build_grid(byte_positions, dim=71, n_bytes=1024)
    print(f"Part One: {shortest_path(grid)}")
    print(f"Part Two: {find_first_blocker(byte_positions, dim=71)}")
