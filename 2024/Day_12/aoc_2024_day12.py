from pathlib import Path

import networkx as nx

from helpers.geometry import MoveDir, iter_neighbors
from helpers.parsing import parse_map_objects


def build_plant_graph(plant_map: str) -> nx.Graph:
    """
    Parse the provided garden map and generate a graph of its components.

    Garden maps are assumed to be an ASCII grid of plots, where each letter represents a different
    type of plant.

    This map, for example, denotes a garden with 5 different plant types:

    ```
    AAAA
    BBCD
    BBCC
    EEEC
    ```

    Note that plants may be present in multiple non-connected regions, e.g.:

    ```
    OOOOO
    OXOXO
    OOOOO
    OXOXO
    OOOOO
    ```

    The generated graph contains edges between individual plots (nodes) if their plant type is
    equivalent.
    """
    pg = nx.Graph()
    for c, v in parse_map_objects(plant_map):
        pg.add_node(c, plant_type=v)

    for node in pg.nodes:
        for n in iter_neighbors(node):
            if n in pg:
                if pg.nodes[node]["plant_type"] == pg.nodes[n]["plant_type"]:
                    pg.add_edge(node, n)

    return pg


def calculate_fence_cost(plant_graph: nx.Graph) -> int:
    """
    Calculate the total fencing cost for the provided garden.

    The fencing price for each individual region is calculated by multiplying that region's area
    by its perimeter.
    """
    total_cost = 0
    for region in nx.connected_components(plant_graph):
        area = len(region)

        perimeter = 0
        for n in region:
            perimeter += 4 - plant_graph.degree[n]

        total_cost += area * perimeter

    return total_cost


def calculate_bulk_fence_cost(plant_graph: nx.Graph) -> int:
    """
    Calculate the bulk discount fencing cost for the provided garden.

    Under the bulk discount, instead of using the perimeter to calculate the price, the number of
    sides each region has is used instead. Each straight section of fence counts as a side,
    regardless of how long it is.
    """
    total_cost = 0
    for region in nx.connected_components(plant_graph):
        area = len(region)

        # Because every corner is a joint between sides, for a closed polygon there is a 1:1
        # relation between sides and corners. We can iterate through possible neighbors that would
        # form both the inner and outer corners and create a count.
        n_sides = 0

        # For outer corners, check that both neighbors are not in the region
        OUTER_CORNERS = (
            (MoveDir.NORTH, MoveDir.WEST),
            (MoveDir.NORTH, MoveDir.EAST),
            (MoveDir.SOUTH, MoveDir.EAST),
            (MoveDir.SOUTH, MoveDir.WEST),
        )

        # For inner corners, check that two neighbors are in the region and the diagonal is not
        INNER_CORNERS = (
            (MoveDir.NORTH, MoveDir.WEST, MoveDir.NORTHWEST),
            (MoveDir.NORTH, MoveDir.EAST, MoveDir.NORTHEAST),
            (MoveDir.SOUTH, MoveDir.EAST, MoveDir.SOUTHEAST),
            (MoveDir.SOUTH, MoveDir.WEST, MoveDir.SOUTHWEST),
        )

        for node in region:
            for dir_a, dir_b in OUTER_CORNERS:
                if all(
                    (
                        dir_a.shift(node) not in region,
                        dir_b.shift(node) not in region,
                    )
                ):
                    n_sides += 1

            for dir_a, dir_b, diag in INNER_CORNERS:
                if all(
                    (
                        dir_a.shift(node) in region,
                        dir_b.shift(node) in region,
                        diag.shift(node) not in region,
                    )
                ):
                    n_sides += 1

        total_cost += area * n_sides

    return total_cost


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    pg = build_plant_graph(puzzle_input)

    print(f"Part One: {calculate_fence_cost(pg)}")
    print(f"Part Two: {calculate_bulk_fence_cost(pg)}")
