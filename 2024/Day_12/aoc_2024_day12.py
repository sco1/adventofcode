from pathlib import Path

import networkx as nx

from helpers.geometry import iter_neighbors
from helpers.parsing import parse_map_objects


def build_plant_graph(plant_map: str) -> nx.Graph:
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
    total_cost = 0
    for region in nx.connected_components(plant_graph):
        area = len(region)

        perimeter = 0
        for n in region:
            perimeter += 4 - plant_graph.degree[n]

        total_cost += area * perimeter

    return total_cost


def calculate_bulk_fence_cost(plant_graph: nx.Graph) -> int:
    raise NotImplementedError


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    pg = build_plant_graph(puzzle_input)

    print(f"Part One: {calculate_fence_cost(pg)}")
    print(f"Part Two: {...}")
