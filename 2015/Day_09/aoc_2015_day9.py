import re
from itertools import permutations
from pathlib import Path
from typing import List, Tuple

import networkx as nx


def process_route(route_list: List[str]) -> List[List]:
    """
    Process Santa's route into a list of lists with the necessary information to build a graph.

    Input is assumed to be of the form: "Faerun to Tristram = 65"

    Output lists are provided as: [source, destination, {"distance": distance], where source and
    destination are str and distance is int
    """
    exp = r"(\w+) to (\w+) = (\d+)"

    edge_list = []
    for edge in route_list:
        source, destination, distance = re.findall(exp, edge)[0]  # Denest the tuple

        # Build the list in a format that nx.Graph is expecting for a weighted edge
        edge_list.append([source, destination, {"distance": int(distance)}])

    return edge_list


def find_route_min_max(santas_route: nx.Graph) -> Tuple[int]:
    """Find the length of the shortest & longest paths that visit every location once."""
    route_summary = []
    # Iterate over all combinations of the nodes and calculate the distance if they form a path
    for route in permutations(list(santas_route.nodes)):
        if nx.is_simple_path(santas_route, route):
            route_distance = sum(
                [
                    santas_route.get_edge_data(*node_pair)["distance"]
                    for node_pair in zip(route, route[1:])
                ]
            )
            route_summary.append([route, route_distance])

    # Sort by distance and return the min & max
    route_summary.sort(key=lambda x: x[1])
    return route_summary[0][1], route_summary[-1][1]


puzzle_input_file = Path("./puzzle_input.txt")
with puzzle_input_file.open(mode="r") as f:
    puzzle_input = f.readlines()

santas_route = nx.Graph(process_route(puzzle_input))
print(find_route_min_max(santas_route))
