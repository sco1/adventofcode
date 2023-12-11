from enum import StrEnum
from pathlib import Path

import networkx as nx

from helpers.geometry import COORD


class PipeLegend(StrEnum):  # noqa: D101
    VERTICAL = "|"
    HORIZONTAL = "-"
    NE_BEND = "L"
    NW_BEND = "J"
    SW_BEND = "7"
    SE_BEND = "F"


CONNECTIONS = {
    PipeLegend.VERTICAL: ((0, -1), (0, 1)),
    PipeLegend.HORIZONTAL: ((-1, 0), (1, 0)),
    PipeLegend.NE_BEND: ((0, -1), (1, 0)),
    PipeLegend.NW_BEND: ((0, -1), (-1, 0)),
    PipeLegend.SW_BEND: ((0, 1), (-1, 0)),
    PipeLegend.SE_BEND: ((0, 1), (1, 0)),
}


def parse_map(map_sketch: str) -> tuple[dict[COORD, str], COORD]:
    """
    Parse the provided 2D pipe map into a directional graph representation of the pipe network.

    Pipe locations are denoted using the characters enumerated by `PipeLegend`, which map to
    different connection locations as specified by the `CONNECTIONS` lookup dictionary. Empty tiles
    are denoted by `.`, and the animal's start location is denoted by `S`.

    The animal's start location is assumed to contain a pipe of an unknown type, but does connect to
    two of its neighbors.

    The map is assumed to contain one complete loop from the starting point.
    """
    animal_start = (-1, -1)
    pipe_graph = nx.DiGraph()
    for y, line in enumerate(map_sketch.splitlines()):
        for x, c in enumerate(line):
            if c == ".":
                continue

            pipe_graph.add_node((x, y))
            if c == "S":
                animal_start = (x, y)
                continue

            for connection_delta in CONNECTIONS[PipeLegend(c)]:
                dx, dy = connection_delta
                pipe_graph.add_edge((x, y), (x + dx, y + dy))

    # Connect animal start point to one of its neighbors to complete the loop
    animal_incoming = list(pipe_graph.in_edges(animal_start))
    pipe_graph.add_edge(animal_start, animal_incoming[0][0])

    return pipe_graph, animal_start


def find_furthest_loop_point(pipe_graph: nx.DiGraph, animal_start: COORD) -> int:
    """
    Locate the number of steps taken to reach the point in the pipe loop furthest from the start.

    It is assumed that the provided pipe network contains at most one complete loop from the start
    location.
    """
    animal_incoming = list(pipe_graph.in_edges(animal_start))

    main_loop = nx.shortest_path(pipe_graph, source=animal_start, target=animal_incoming[1][0])
    return len(main_loop) // 2


def n_enclosed_tiles(pipe_graph: nx.DiGraph) -> int:
    """
    Calculate the number of empty tiles enclosed by the provided pipe map.

    It is assumed that the provided pipe network contains at most one complete loop.

    "Squeezing" in between pipes is allowed, so a region may still be considered fully enclosed even
    if it does not contain a path to the boundary of the mapped region.
    """
    ...


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    pipe_graph, animal_start = parse_map(puzzle_input)
    print(f"Part One: {find_furthest_loop_point(pipe_graph, animal_start)}")
    print(f"Part Two: {n_enclosed_tiles(pipe_graph)}")
