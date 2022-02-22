import re
from itertools import permutations, zip_longest
from pathlib import Path
from typing import List, Set, Tuple

import networkx as nx


def parse_seating_instructions(
    instructions: List[str], include_self: bool = False
) -> Tuple[Set, nx.DiGraph]:
    """
    Parse the dinner party's seating arrangements into attendees' seating preferences.

    Instructions are assumed to be of the form:
        "A would gain|lose X happiness units by sitting next to B"

    Optinally include yourself in the dinner party, where your happiness gain/loss is 0 to others.

    Output is a set representing the guest list and a DiGraph representing the happiness gain/loss
    for each person based on who they're sitting next to.
    """
    exp = r"(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+)"
    preference_digraph = nx.DiGraph()
    for instruction in instructions:
        seating_preference = re.findall(exp, instruction)[0]  # Denest tuple

        # Use happiness gain/loss as the edge weight
        if seating_preference[1] == "gain":
            edge_weight = int(seating_preference[2])
        else:
            edge_weight = -int(seating_preference[2])

        preference_digraph.add_edge(
            seating_preference[0], seating_preference[-1], happiness=edge_weight
        )

    guest_list = set(preference_digraph.nodes)

    if include_self:
        # To include ourself in the dinner party, add edges to/from everyone else with 0 weight
        preference_digraph.add_edges_from(
            zip_longest(guest_list, ["Self"], fillvalue="Self"), happiness=0
        )
        preference_digraph.add_edges_from(
            zip_longest(["Self"], guest_list, fillvalue="Self"), happiness=0
        )
        guest_list.add("Self")

    return guest_list, preference_digraph


def calculate_happiness(seating_arrangement: Tuple[str], preference_DiGraph: nx.DiGraph) -> int:
    """Calculate the happiness of a given seating arrangement based on the preference DiGraph."""
    happiness_score = 0
    for left, right in zip(seating_arrangement, seating_arrangement[1:]):
        happiness_score += preference_DiGraph.get_edge_data(left, right)["happiness"]
        happiness_score += preference_DiGraph.get_edge_data(right, left)["happiness"]

    # Wrap tails
    left, right = seating_arrangement[0], seating_arrangement[-1]
    happiness_score += preference_DiGraph.get_edge_data(left, right)["happiness"]
    happiness_score += preference_DiGraph.get_edge_data(right, left)["happiness"]

    return happiness_score


def find_optimal_seating(instructions: List[str], include_self: bool = False) -> int:
    """
    Find the optimal (maximum happiness) seating arrangements given the input seating instructions.

    Optinally include yourself in the dinner party, where your happiness gain/loss is 0 to others.

    Table is assumed to be circular.
    """
    guest_list, preference_DiGraph = parse_seating_instructions(instructions, include_self)
    return max(
        calculate_happiness(arrangement, preference_DiGraph)
        for arrangement in permutations(guest_list)
    )


puzzle_input_file = Path("./puzzle_input.txt")
with puzzle_input_file.open(mode="r") as f:
    puzzle_input = f.readlines()


print(find_optimal_seating(puzzle_input))
print(find_optimal_seating(puzzle_input, include_self=True))
