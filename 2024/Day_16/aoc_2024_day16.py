from pathlib import Path

import networkx as nx

from helpers.geometry import COORD, MoveDir
from helpers.parsing import parse_map_objects

ROTS = (MoveDir.NORTH, MoveDir.EAST, MoveDir.SOUTH, MoveDir.WEST)


def parse_reindeer_map(raw_map: str) -> tuple[nx.DiGraph, COORD]:
    """
    Parse the provided Reindeer Maze map into its digraph representation.

    The maze is assumed to be presented as an ASCII grid where wall locations are marked with `#`,
    empty tiles marked by `.`, start location is marked by `S`, and the finish line marked by `E`.

    The maze tiles are represented as nodes in the graph, and edge weights for calculating maze
    traversal score are included.
    """
    start: COORD | None = None
    finish: COORD | None = None

    maze = nx.DiGraph()
    for loc, c in parse_map_objects(raw_map, empty_tile="#"):
        if c == "S":
            start = loc
        if c == "E":
            finish = loc

        # Encode the direction in each node so we can weight the edges
        for d in ROTS:
            maze.add_node((loc, d))

    if start is None:
        raise ValueError("Could not locate start location")
    if finish is None:
        raise ValueError("Could not locate finish location")

    # For each node, connect same-facing directions with a weight of 1, and edges that require a 90
    # degree turn with a weight of 1000 to provide the scoring incurred for rotation
    for loc, d in maze.nodes:
        if (d.shift(loc), d) in maze.nodes:
            maze.add_edge((loc, d), (d.shift(loc), d), weight=1)

        for rot in (d.rot_90(), d.rot_90(reverse=True)):
            maze.add_edge((loc, d), (loc, rot), weight=1000)

    # Add a labeled 0-weight dummy node connected to any adjacent node to serve as a more easily
    # referenced finish line target
    for d in ROTS:
        maze.add_edge((finish, d), "finish", weight=0)

    return maze, start


def calculate_lowest_score(
    maze: nx.DiGraph, start: COORD, start_dir: MoveDir = MoveDir.EAST
) -> int:
    """
    Calculate the lowest possible score for a reindeer traversing the Olympic Reindeer Maze.

    While traversing the maze from the Starting tile (facing East) to the Finish tile, the reindeer
    gains one point for each move forward, and 1000 points for each 90 degree rotation required to
    continue moving towards the goal.

    NOTE: It is assumed that the scores have already been included in the maze graph as edge
    weights.
    """
    # Because we've already encoded the turn weights into the edges we don't need to do any walking
    # ourselves & can just let NetworkX fire away :)
    return nx.shortest_path_length(maze, (start, start_dir), "finish", weight="weight")


def n_seat_locations(maze: nx.DiGraph, start: COORD, start_dir: MoveDir = MoveDir.EAST) -> int:
    """Calculate the number of tiles that are on at least 1 best path through the reindeer maze."""
    # Probably not the most elegant way but we can just make a set of our seen coordinates and
    # iterate through all of the shortest paths to get our count, it finishes eventually!
    seen_coords = set()
    for p in nx.all_shortest_paths(maze, (start, start_dir), "finish", weight="weight"):
        # Skip the last node so we're not including our dummy finish line node
        for n in p[:-1]:
            seen_coords.add(n[0])

    return len(seen_coords)


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    maze, start = parse_reindeer_map(puzzle_input)

    print(f"Part One: {calculate_lowest_score(maze, start)}")
    print(f"Part Two: {n_seat_locations(maze, start)}")
