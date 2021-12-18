import math
import typing as t
from collections import defaultdict
from heapq import heappop, heappush
from pathlib import Path

COORDINATE = tuple[int, int]
MAP = dict[COORDINATE, int]


def _wrap_risk(risk: int) -> int:
    """Wrap risk levels that are higher than 9 back to 1 instead of 0."""
    rem = risk % 9
    if rem == 0:
        return 9

    return rem


def parse_risk_map(raw_map: list[str], tiled: bool = False) -> tuple[MAP, COORDINATE]:
    """
    Parse the provided risk map into a dictionary mapping risk level to coordinate.

    If the `tiled` flag is set, then the map is parsed assuming that the map expands into a 5x5
    tiled grid. The given map tile repeats to the right and downward; each time the tile repeats to
    the right or downward, all of its risk levels are 1 higher than the tile immediately up or left
    of it. Risk levels above 9 wrap back around to 1.

    The bottom right location is also returned to skip needing to get the map size downstream.
    """
    risk_map = {}
    for y, line in enumerate(raw_map):
        for x, risk_level in enumerate(line):
            if not tiled:
                risk_map[(x, y)] = int(risk_level)
            else:
                width = len(raw_map[0])
                height = len(raw_map)
                for y_tile in range(5):
                    for x_tile in range(5):
                        x_idx = x + (x_tile * width)
                        y_idx = y + (y_tile * height)
                        risk_map[(x_idx, y_idx)] = _wrap_risk(int(risk_level) + (x_tile + y_tile))

    if tiled:
        x, y = x_idx, y_idx

    return risk_map, (x, y)


def iter_neighbors(x: int, y: int) -> t.Generator[COORDINATE, None, None]:
    """
    Iterate over the vertical & lateral neighbor coordinates (LRUD) of the provided center point.

    This is a graceful & different approach from what I've done previously with lambdas or some
    other slicing techniques to get neighbors, so I wanted to give it a whirl!

    I did not write this, it's taken from @asottile's solve on stream:
        https://www.youtube.com/watch?v=8_9I6fNR7Z8
        https://github.com/anthonywritescode/aoc2021/blob/main/day15/part1.py#L15-L19
    """
    yield x - 1, y
    yield x + 1, y
    yield x, y - 1
    yield x, y + 1


def find_route(risk_map: MAP, destination: COORDINATE) -> int:
    """
    Calculate the least risky route to the destination using the provided risk map.

    The start point & origin `(0, 0)` is assumed to be the top left of the map.

    NOTE: It is assumed that the submarine cannot move diagonally.
    """
    # Time for some Dijkstra! https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    # Per the problem description cost is added when a position is entered, so we start at 0
    heap = [(0, (0, 0))]  # distance (risk), node
    min_risk = defaultdict(lambda: math.inf, {(0, 0): 0})
    seen = set()
    while heap:
        # Use heapq, as we want to select the next unvisited node with the lowest potential distance
        risk, node = heappop(heap)

        if node == destination:
            return risk

        if node in seen:
            continue

        # For each node we visit, we check its unvisited neighbors & find the shortest distance
        # (risk) to the starting node & update the current node accordingly
        seen.add(node)
        for neighbor_coord in iter_neighbors(*node):
            if neighbor_coord not in risk_map:
                continue

            tentative_risk = risk + risk_map[neighbor_coord]
            if tentative_risk < min_risk[neighbor_coord]:
                min_risk[neighbor_coord] = tentative_risk
                heappush(heap, (tentative_risk, neighbor_coord))


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().splitlines()

    print(f"Part One: {find_route(*parse_risk_map(puzzle_input))}")
    print(f"Part Two: {find_route(*parse_risk_map(puzzle_input, True))}")
