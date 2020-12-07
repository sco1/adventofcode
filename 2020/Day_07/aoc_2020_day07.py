import re
from collections import deque
from pathlib import Path

import more_itertools as mi
import networkx as nx


def parse_bag_rule(raw_rule: str) -> list[tuple[str, str, dict[str, int]]]:
    """
    Parse the provided rule string into its source -> content mapping.

    Output is provided as a list of 3-tuples of the form `(source, destination, {"quantity": n})`
    for compatibility with NetworkX

    Rules are assumed to match one of the following patterns:
        * "faded blue bags contain no other bags." (contains no bags)
        * "bright white bags contain 1 shiny gold bag." (contains single bag type)
        * "light red bags contain 1 bright white bag, 2 muted yellow bags." (contains multiple bags)

    Bag colors are assumed to always be two words.
    """
    raw_source, raw_contains = [chunk.strip() for chunk in raw_rule.split("contain")]

    source_pattern = r"(\w+ \w+)"
    source = re.match(source_pattern, raw_source).group(0)

    bag_map = []
    bag_pattern = r"(\d+) (\w+ \w+)"
    if raw_contains != "no other bags.":
        for quantity, color in re.findall(bag_pattern, raw_contains):
            bag_map.append((source, color, {"quantity": int(quantity)}))

    return bag_map


def build_bag_graph(all_rules: list[str]) -> nx.DiGraph:
    """
    Build a directed graph from the provided luggage rules.

    The resulting digraph represents each color-coded luggage type as nodes, with any contents as
    edges between the luggage type and its sub-type(s). Edges contain `"quantity"` data to represent
    the number of bags contained.

    Rules are assumed to match one of the following patterns:
        * "faded blue bags contain no other bags." (contains no bags)
        * "bright white bags contain 1 shiny gold bag." (contains single bag type)
        * "light red bags contain 1 bright white bag, 2 muted yellow bags." (contains multiple bags)
    """
    bag_map = nx.DiGraph()
    bag_map.add_edges_from(mi.flatten(parse_bag_rule(rule) for rule in all_rules))

    return bag_map


def n_valid_bags(bag_map: nx.DiGraph, target_color: str) -> int:
    """Count the number of top-level bag colors that can eventually contain the target color bag."""
    n_valid = 0
    for node in bag_map:
        # Skip the target color since it has a path to itself but doesn't actually contain itself
        if node == target_color:
            continue

        if nx.has_path(bag_map, node, target_color):
            n_valid += 1

    return n_valid


def n_contained_bags(bag_map: nx.DiGraph, outer_bag: str = "shiny gold") -> int:
    """Count the number of bags that must be contained by the provided outer bag."""
    n_bags = -1  # Start at -1 so we don't count the starting bag
    nodes_to_visit = deque((outer_bag,))

    while nodes_to_visit:
        n_bags += 1
        node = nodes_to_visit.popleft()

        edges = bag_map.out_edges(node, data=True)
        for _, sub_bag, data in edges:
            # To account for bag subquantities, add the bag n times to the queue
            nodes_to_visit.extend([sub_bag] * data["quantity"])

    return n_bags


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().splitlines()

    bag_map = build_bag_graph(puzzle_input)
    print(f"Part One: {n_valid_bags(bag_map, 'shiny gold')} matching bags")
    print(f"Part Two: {n_contained_bags(bag_map)} contained bags")
