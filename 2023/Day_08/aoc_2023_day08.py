import itertools
import math
import re
from pathlib import Path

NODE_RE = re.compile(r"(\w+) = \((\w+), (\w+)\)")


def parse_map(raw_map: str) -> tuple[str, dict[str, tuple[str, str]]]:
    """
    Parse the provided desert map and provide the navigation instructions & a collection of nodes.

    The map is assumed to be of the following form:

    ```
    <instructions>

    <node> = (<left>, <right>)
    ...
    ```
    """
    instructions, *raw_nodes = (line for line in raw_map.splitlines() if line)
    nodes = {}
    for node in raw_nodes:
        node_name, left, right = NODE_RE.findall(node)[0]
        nodes[node_name] = (left, right)

    return instructions, nodes


def traverse_map(
    instructions: str,
    desert_map: dict[str, tuple[str, str]],
    start: str = "AAA",
    dest: str = "ZZZ",
) -> int:
    """
    Navigate from the provided start node until the end node has been reached.

    Navigation instructions are assumed to be a pattern of left (`L`) or right (`R`) instructions
    that the map reader follows. The pattern is assumed to loop infinitely, e.g. `RL` -> `RLRL...`.
    """
    n_steps = 0
    curr = start
    for step in itertools.cycle(instructions):
        if curr == dest:
            break

        if step == "L":
            curr = desert_map[curr][0]
        elif step == "R":
            curr = desert_map[curr][1]
        else:
            raise ValueError(f"Unknown step direction: '{step}'")

        n_steps += 1

    return n_steps


def traverse_as_ghost_bf(
    instructions: str,
    desert_map: dict[str, tuple[str, str]],
    start_suffix: str = "A",
    end_suffix: str = "Z",
) -> int:
    """
    Navigate simultaneously from all start nodes until the ending nodes are reached.

    Starting and ending nodes are identified by having names that end with `start_suffix` and
    `end_suffix`, respectively.

    Navigation instructions are assumed to be a pattern of left (`L`) or right (`R`) instructions
    that the map reader follows. The pattern is assumed to loop infinitely, e.g. `RL` -> `RLRL...`.

    WARNING: This algorithm is a brute-force approach and may not work well with challenging node
    mappings.
    """
    n_steps = 0
    curr = [node for node in desert_map if node.endswith(start_suffix)]
    for step in itertools.cycle(instructions):
        if all(loc.endswith(end_suffix) for loc in curr):
            break

        if step == "L":
            curr = [desert_map[loc][0] for loc in curr]
        elif step == "R":
            curr = [desert_map[loc][1] for loc in curr]
        else:
            raise ValueError(f"Unknown step direction: '{step}'")

        n_steps += 1

    return n_steps


def traverse_as_ghost(
    instructions: str,
    desert_map: dict[str, tuple[str, str]],
    start_suffix: str = "A",
    end_suffix: str = "Z",
) -> int:
    """
    Navigate simultaneously from all start nodes until the ending nodes are reached.

    Starting and ending nodes are identified by having names that end with `start_suffix` and
    `end_suffix`, respectively.

    Navigation instructions are assumed to be a pattern of left (`L`) or right (`R`) instructions
    that the map reader follows. The pattern is assumed to loop infinitely, e.g. `RL` -> `RLRL...`.
    """
    # Identify cycles for each ghost, then use GCD to find when they all align
    start_nodes = [node for node in desert_map if node.endswith(start_suffix)]
    cycle_lengths = []
    for node in start_nodes:
        curr = node
        n_steps = 0
        for step in itertools.cycle(instructions):
            if curr.endswith(end_suffix):
                break

            if step == "L":
                curr = desert_map[curr][0]
            elif step == "R":
                curr = desert_map[curr][1]
            else:
                raise ValueError(f"Unknown step direction: '{step}'")

            n_steps += 1

        cycle_lengths.append(n_steps)

    return math.lcm(*cycle_lengths)


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    instructions, nodes = parse_map(puzzle_input)
    print(f"Part One: {traverse_map(instructions, nodes)}")
    print(f"Part Two: {traverse_as_ghost(instructions, nodes)}")
