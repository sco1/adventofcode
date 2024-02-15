from pathlib import Path

import networkx as nx

from helpers.geometry import COORD, iter_neighbors


def parse_garden_map(garden_map: str) -> tuple[set[COORD], set[COORD], COORD]:
    """
    Parse the provided garden map into its plot, rock, and gardener start locations.

    The provided garden map is assumed to consist of rows of characters describing the contents of
    each point in the garden. A location may hold a garden plot (`.`), a rock (`#`), or the
    gardener's starting location (`S`). There is assumed to be only one gardener start location, and
    it is also considered a garden plot.
    """
    start = (-1, -1)
    plots = set()
    rocks = set()
    for y, line in enumerate(garden_map.splitlines()):
        for x, c in enumerate(line):
            coord = (x, y)
            if c == ".":
                plots.add(coord)
            elif c == "#":
                rocks.add(coord)
            elif c == "S":
                # Starting point counts as a garden plot
                plots.add(coord)
                start = coord

    return plots, rocks, start


def build_garden_network(plots: set[COORD], rocks: set[COORD]) -> nx.Graph:
    """
    Generate a graph from the provided garden plot locations.

    Plots are considered connected if they share a side along any cardinal direction; diagonals are
    not considered.
    """
    plots_graph = nx.Graph()
    for p in plots:
        for n in iter_neighbors(p):
            if n in plots:
                plots_graph.add_edge(p, n)

    return plots_graph


def step_search(garden_network: nx.Graph, start: COORD, n_steps: int = 64) -> set[COORD]:
    """Determine the garden plots reachable after `n_steps` from the start location."""
    visited_plots = {(start,)}
    for _ in range(n_steps):
        neighbors = set()
        for p in visited_plots:
            neighbors.update(garden_network.neighbors(p))

        visited_plots = neighbors

    return visited_plots


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    plots, rocks, start = parse_garden_map(puzzle_input)
    n = build_garden_network(plots, rocks)
    print(f"Part One: {len(step_search(n, start))}")
    print(f"Part Two: {...}")
