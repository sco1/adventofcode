import itertools
import math
import typing as t
from collections import abc
from pathlib import Path

import networkx as nx

from helpers.geometry import euclidean_distance

COORD_3D_T: t.TypeAlias = tuple[int, int, int]


def parse_junctions(junction_map: str) -> list[COORD_3D_T]:
    """
    Parse the provided junction map into a list of junction coordinates in 3D space.

    Junctions are assumed to be provided as newline delimited 3D `X,Y,Z` coordinates.
    """
    junctions = []
    for line in junction_map.splitlines():
        x, y, z = line.split(",")
        junctions.append((int(x), int(y), int(z)))

    return junctions


def junction_pdist(
    junctions: abc.Iterable[COORD_3D_T],
) -> list[tuple[float, COORD_3D_T, COORD_3D_T]]:
    """Calculate the pairwise distance between the provided junctions, sorted in ascending order."""
    distances = sorted(
        (euclidean_distance(p, q), p, q) for p, q in itertools.combinations(junctions, 2)
    )
    return distances


def connect_n_closest(junctions: abc.Iterable[COORD_3D_T], n: int = 1000) -> int:
    """Connect the `n` closest junctions together and measure the size of the 3 largest circuits."""
    pdist = junction_pdist(junctions)
    circuit = nx.Graph()

    for connected_pair in pdist[:n]:
        _, p, q = connected_pair
        circuit.add_edge(p, q)

    # Circuits will be connected components of the connection graph
    circuit_sizes = sorted((len(comp) for comp in nx.connected_components(circuit)), reverse=True)
    return math.prod(circuit_sizes[:3])


def connect_all(junctions: abc.Iterable[COORD_3D_T]) -> int:
    """
    Iterate through & connect pairs of junctions by distance until a complete circuit is formed.

    Once a complete circuit is formed, measure the extension cable distance by multiplying together
    the X coordinates of the last connected junction pair.
    """
    pdist = junction_pdist(junctions)
    circuit = nx.Graph()
    circuit.add_nodes_from(junctions)

    # Add pairs until we end up with a connected graph
    for connected_pair in pdist:
        _, p, q = connected_pair
        circuit.add_edge(p, q)

        if nx.is_connected(circuit):
            return p[0] * q[0]

    raise ValueError("Could not connect all junctions to a single circuit")


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    junctions = parse_junctions(puzzle_input)

    print(f"Part One: {connect_n_closest(junctions)}")
    print(f"Part Two: {connect_all(junctions)}")
