import collections
import re
from pathlib import Path

import networkx as nx

NODE_RE = re.compile(r"(\w+)\s+\((\d+)\)")


def _build_tower(programs: list[str]) -> nx.DiGraph:
    """
    Construct a digraph from the provided program responses.

    Responses are assumed to be of the following forms:
        * `pbga (66)`
        * `fwft (72) -> ktlj, cntj, xhth`

    Where `<name> (<weight>)` provides the node information and `-> <name(s)>`, if present provides
    any edges (comma separated) from the node.
    """
    tower = nx.DiGraph()
    for response in programs:
        node_info, _, edges = response.partition(" -> ")
        node, weight = NODE_RE.findall(node_info)[0]
        tower.add_node(node, weight=int(weight))

        # Add edges if we've found any
        if edges:
            for dest in edges.split(","):
                tower.add_edge(node, dest.strip())

    return tower


def find_bottom_program(tower: nx.DiGraph) -> str:
    """
    Locate the base of the program tower described by the provided program responses.

    Responses are assumed to be of the following forms:
        * `pbga (66)`
        * `fwft (72) -> ktlj, cntj, xhth`

    Where `<name> (<weight>)` provides the node information and `-> <name(s)>`, if present provides
    any edges (comma separated) from the node.
    """
    # The base of the tower should have an in degree of 0 since it only has outward edges
    for node, in_degree in tower.in_degree:
        if in_degree == 0:
            return node


def balance_tower(tower: nx.DiGraph) -> int:
    """
    Locate the incorrectly weighted program and calculate the weight needed to rebalance the tower.

    For any program holding a disc, each program standing on the disk forms a sub-tower. Each of
    these sub-towers needs to be the same weight, or the disc isn't balanced. The weight of a tower
    is the sum of the weights of the programs in the tower.

    NOTE: It is assumed that there is only one incorrectly weighted program for the provided tower.
    """
    # To check for balance, start with the leaves of the tower & work downward to the base, storing
    # the sub-tower weights as we go along in order to find the black sheep node
    # A reversed topological sort gets us to the leaves first
    seen_weights = {}
    for node in reversed(list(nx.topological_sort(tower))):
        # Init the sub-tower weight with its base node
        sub_tower_weight = tower.nodes[node]["weight"]

        # Populate the seen sub-tower weights
        # This will start empty at the leaves and populate as we traverse towards the base
        weight_counts = collections.Counter(seen_weights[child] for child in tower[node])

        black_sheep = None
        for supported in tower[node]:
            # If this node is supporting multiple sub-towers then each sub-tower must have the same
            # weight. Since there is assumed to be only one mismatched weight, if we're supporting
            # more than one sub-tower and we have a unique weight, then this is the black sheep
            if len(weight_counts) > 1 and weight_counts[seen_weights[supported]] == 1:
                black_sheep = supported
                break

            # Otherwise we can calculate the total sub-tower weight and add it to what we've seen
            sub_tower_weight += seen_weights[supported]

        if black_sheep is not None:
            # If we've gotten here then we have at least one sub-tower at this level to compare
            # the correct weight to
            # Get rid of the black sheep weight from the counts to guard against a base with only 2
            # edges
            weight_counts.pop(seen_weights[supported])
            target_weight, _ = weight_counts.most_common(1)[0]
            delta = target_weight - seen_weights[supported]
            return tower.nodes[black_sheep]["weight"] + delta

        # Otherwise, update the subtower & continue our trek
        seen_weights[node] = sub_tower_weight


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().splitlines()
    tower = _build_tower(puzzle_input)

    print(f"Part One: {find_bottom_program(tower)}")
    print(f"Part Two: {balance_tower(tower)}")
