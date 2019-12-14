from pathlib import Path
from typing import List

import networkx as nx


def system_from_orbits(orbits: List[str]) -> nx.Graph:
    """
    Build a graph of the solar system from the provided list of orbits.

    Orbits are provided as "orbited)orbiter" strings, where `)` is used to delimit between orbited
    and orbiter
    """
    system = nx.Graph()
    system.add_edges_from(orbit.split(")") for orbit in orbits)

    return system


def n_total_orbits(solar_system: nx.Graph) -> int:
    """Find the total number of direct and indirect orbits in the solar system."""
    # If source is provided without a target, nx.shortest_path_length will return a dict with
    # (target, shortest path to target) key,value pairs for all nodes in the graph. If we sum these
    # then we can capture all direct and indirect orbits
    return sum(nx.shortest_path_length(solar_system, source="COM").values())


def get_to_santa(solar_system: nx.Graph) -> int:
    """Find the shortest path from the body we are orbiting to the one Santa is orbiting."""
    # Subtract 2 to null out our orbit & Santa's orbit
    return nx.shortest_path_length(solar_system, source="YOU", target="SAN") - 2


if __name__ == "__main__":
    puzzle_input = Path("./puzzle_input.txt")

    with puzzle_input.open("r") as f:
        orbital_map = [line.strip() for line in f]

    solar_system = system_from_orbits(orbital_map)

    # Part 1
    print(n_total_orbits(solar_system))

    # Part 2
    print(get_to_santa(solar_system))
