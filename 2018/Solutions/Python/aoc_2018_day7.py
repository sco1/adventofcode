import re
from pathlib import Path
from typing import List

import networkx as nx


def part1(puzzle_input: List[str]) -> str:
    """
    Topological sort!
    """
    DG = nx.DiGraph()
    DG.add_edges_from(puzzle_input)

    out_path = []
    start_nodes = sorted([node for node in DG.nodes if DG.in_degree(node) == 0], reverse=True)
    while len(start_nodes) > 0:
        start = start_nodes.pop()
        out_path.append(start)

        neighbors = sorted(DG.neighbors(start))
        for neighbor in neighbors:
            DG.remove_edge(start, neighbor)

            if DG.in_degree(neighbor) == 0:
                start_nodes.append(neighbor)
                start_nodes.sort(reverse=True)

    return "".join(out_path)


puzzle_input_file = Path("../../Inputs/puzzle_input_d7.txt")
with puzzle_input_file.open(mode="r") as f:
    """
    Parse the input lines

    Group 1: Step that must be finished
    Group 2: Step to begin
    """
    exp = r"(?<=[Ss]tep\s)(\w)"
    puzzle_input = [re.findall(exp, line) for line in f]

print(part1(puzzle_input))
