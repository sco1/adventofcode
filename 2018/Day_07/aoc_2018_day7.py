import re
from pathlib import Path

import networkx as nx

STEP_RE = re.compile(r"[Ss]tep (\w)")


def _parse_edges(instructions: list[str]) -> list[list[str]]:
    """
    Parse the provided instructions into a list of edges.

    Instructions are assumed to be of the form:
        * `Step <node> must be finished before step <node> can begin.`

    Where nodes are designated by a single letter.
    """
    return [STEP_RE.findall(line) for line in instructions]


def determine_step_order(edges: list[list[str]]) -> str:
    """
    Determine the order in which the provided instructions should be completed.

    The provided instructions describe the series of steps and requirements about which steps must
    be finished before others can begin. If more than one step is ready, the step that is first
    alphabetically is chosen.
    """
    # This is just a lexicographical topological sort
    graph = nx.DiGraph()
    graph.add_edges_from(edges)

    return "".join(nx.lexicographical_topological_sort(graph))


def elf_assembly(edges: list[list[str]], n_workers: int = 5, base_time: int = 60) -> int:
    """
    Calculate the time required for the elves to construct Santa's sleigh.

    Each step takes `base_time` seconds plus an amount corresponding to its letter (e.g. `A=1`,
    `B=2`, `C=3`, ...). If multiple steps are available, workers begin them in alphabetical order.
    """
    # Construct the graph & add in each node's time to completion
    graph = nx.DiGraph()
    graph.add_edges_from(edges)
    for node in graph.nodes:
        time_offset = ord(node) - ord("A") + 1  # A=1, B=2, etc.
        graph.nodes[node]["worktime"] = base_time + time_offset

    timestep = 0
    while graph.nodes:
        # If a step's prerequisites are complete then it won't have any incoming edges
        # Per the problem spec, sort available nodes alphabetically
        available = [node for node in graph.nodes if graph.in_degree(node) == 0]
        available.sort()

        # Assign available steps to workers
        # Use zip so we limit the selected nodes to the number of workers
        for _, node in zip(range(n_workers), available):
            graph.nodes[node]["worktime"] -= 1

            # Pop node if the step is completed
            if graph.nodes[node]["worktime"] == 0:
                graph.remove_node(node)

        timestep += 1

    return timestep


if __name__ == "__main__":
    puzzle_input_file = Path("puzzle_input.txt")
    instructions = puzzle_input_file.read_text().splitlines()

    edges = _parse_edges(instructions)
    print(f"Part One: {determine_step_order(edges)}")
    print(f"Part Two: {elf_assembly(edges)}")
