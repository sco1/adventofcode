import math
from itertools import permutations
from pathlib import Path

import networkx as nx


def build_graph(puzzle_input: str) -> nx.DiGraph:
    """
    Parse the provided bag of adapters into a valid charging graph.

    The charging graph is an acyclical directed graph where an edge exists between the adapter nodes
    if the difference in joltage is between 1 and 3, inclusive. The power outlet & device are also
    added as nodes in the graph. The joltage `"delta"` is stored as addional data in the edge.
    """
    adapter_graph = nx.DiGraph()
    adapter_graph.add_nodes_from(int(line) for line in puzzle_input.splitlines())

    # Add outlet (0) and device (3 higher than max adapter)
    adapter_graph.add_nodes_from((0, max(adapter_graph.nodes) + 3))

    # Add edges between adapters where the delta is [1, 3] joltage
    for source, dest in permutations(adapter_graph.nodes, 2):
        delta = dest - source
        if 1 <= delta <= 3:
            adapter_graph.add_edge(source, dest, delta=delta)  # Store the delta for later

    return adapter_graph


def find_adapter_chain(adapter_graph: nx.DiGraph) -> tuple[int, int]:
    """Find a valid chain of adapters & determine how many 1 & 3 joltage deltas are present."""
    # NOTE: This approach is super overkill for this problem, but I wanted to stick with the graph
    #
    # Since our edges represent a valid adapter connection, we're looking for a Hamiltonian path
    # here: a path that visits every node exactly once. For this problem, since adapter joltage has
    # to be ascending, we can check a topological sort and see if they're all connected.
    n_one_delta = 0
    n_three_delta = 0
    for check_path in nx.all_topological_sorts(adapter_graph):
        # First check that the topological sort has yielded a valid path.
        if not nx.is_path(adapter_graph, check_path):
            continue

        # Let's assume there's only one valid path
        for source, dest in zip(check_path, check_path[1:]):
            delta = adapter_graph.get_edge_data(source, dest)["delta"]
            if delta == 1:
                n_one_delta += 1
            elif delta == 3:
                n_three_delta += 1

    return n_one_delta, n_three_delta


def n_paths(adapter_graph: nx.DiGraph) -> int:
    """Calculate the total number of valid adapter combinations."""
    # Use the adjacency matrix to count the number of paths from the outlet to the device
    # We can assume that there are no cycles
    # int32 may overflow for larger inputs, int64 seems to be safe
    adj = nx.adjacency_matrix(adapter_graph).astype("int64")

    # The adjacency matrix method returns a sparse matrix whose rows & columns are indexed based on
    # the order of the nodes. Since we appended the outlet & device to the graph after the adapters,
    # they'll be the last two indices
    n_nodes = len(adapter_graph.nodes)
    outlet_idx = n_nodes - 2
    device_idx = n_nodes - 1

    return sum((adj**n)[outlet_idx, device_idx] for n in range(1, n_nodes))


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text()

    adapter_graph = build_graph(puzzle_input)
    print(f"Part One: {math.prod(find_adapter_chain(adapter_graph))}")
    print(f"Part Two: {n_paths(adapter_graph)} possible combinations")
