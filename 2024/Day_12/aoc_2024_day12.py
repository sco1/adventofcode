from pathlib import Path

import networkx as nx

from helpers.geometry import iter_neighbors
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
    raise NotImplementedError


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    pg = build_plant_graph(puzzle_input)

    print(f"Part One: {calculate_fence_cost(pg)}")
    print(f"Part Two: {...}")
