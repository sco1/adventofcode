from collections import deque
from pathlib import Path

import networkx as nx


def build_nodes(
    puzzle_input: deque, idx: int = 0, dg: nx.DiGraph | None = None
) -> tuple[nx.DiGraph, int]:
    """
    Recurse & build the tree from the input puzzle_data.

    Thanks PyDis user Phoenix#2694 for fixing my recursion <3
    """
    if dg is None:
        dg = nx.DiGraph()

    n_child_nodes = puzzle_input.popleft()
    n_metadata_entries = puzzle_input.popleft()

    parent_idx = idx
    for _ in range(n_child_nodes):
        # Recurse here to account for child nodes
        dg, idx = build_nodes(puzzle_input, idx, dg)
        dg.add_edge(parent_idx, idx)

    # Once we get here we should only have metadata to pop
    node_metadata = []
    for _ in range(n_metadata_entries):
        node_metadata.append(puzzle_input.popleft())

    # print(idx, node_metadata)
    dg.add_node(idx, metadata=node_metadata)

    return dg, idx + 1


def part1(tree: nx.DiGraph) -> int:
    """Calculate the sum of all of the node's metadata."""
    metadata_sum = 0
    tree_metadata = nx.get_node_attributes(tree, "metadata")

    for metadata in tree_metadata.values():
        metadata_sum += sum(metadata)

    return metadata_sum


if __name__ == "__main__":
    puzzle_input_file = Path("puzzle_input.txt")
    with puzzle_input_file.open(mode="r") as f:
        puzzle_input = deque([int(x) for x in f.read().strip().split()])

    tree, _ = build_nodes(puzzle_input)
    print(part1(tree))
