from __future__ import annotations

import math
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, NamedTuple


class Reaction(NamedTuple):
    """Represent a reaction that the nanofactory can perform."""

    product: str
    n_out: int
    reactants: Dict[str, int]

    @classmethod
    def from_str(cls, reaction_str: str) -> Reaction:
        """
        Build a reaction object from the provided reaction string.

        Reaction strings are assumed to be of the form `'7 A, 1 E => 1 FUEL'`
        """
        reactant_str, product_str = reaction_str.split("=>")

        n_out, product = product_str.split()
        reactants = Reaction.parse_reactants(reactant_str)

        return cls(product, int(n_out), reactants)

    @staticmethod
    def parse_reactants(reactant_str: str) -> Dict[str, int]:
        """Parse reactants into a dictionary with reactant, quantity k,v pairs."""
        reactants = {}
        for raw_reactant in reactant_str.split(", "):
            reactant_quantity, reactant = raw_reactant.split()
            reactants[reactant] = int(reactant_quantity)

        return reactants

    @staticmethod
    def from_reaction_list(reaction_list: List[str]) -> Dict[str, Reaction]:
        """Parse the provided reaction list into a dictionary with product, Reaction k,v pairs."""
        reactions = (Reaction.from_str(reaction_str) for reaction_str in reaction_list)
        return {reaction.product: reaction for reaction in reactions}


def react_for_fuel(reactions: Dict[str, Reaction], fuel_req: int = 1) -> int:
    """Calculate the amount of input ORE required to react for the required fuel quantity."""
    # Use a defaultdict to track our supply & demand
    # Where quantity < 0 is supply and quantity > 0 is demand
    ingredient_store = defaultdict(int)
    ingredient_store["FUEL"] = fuel_req

    # My assignment operator!
    # Iterate over the required ingredients & react them as needed until we satisfy the fueldemand
    # Ignore ORE since it's our input ingredient & can't be reacted for
    while any(
        (chemical := ingredient)
        for ingredient, demand in ingredient_store.items()
        if ingredient != "ORE" and demand > 0
    ):
        # From the problem statement, we can assume there is only one reaction for a given chemical
        reaction, quantity_needed = reactions[chemical], ingredient_store[chemical]
        n_runs = math.ceil(quantity_needed / reaction.n_out)  # Surplus is ok

        # Add the required reactants to our ingredient demand
        for reactant, reactant_needed in reaction.reactants.items():
            ingredient_store[reactant] += n_runs * reactant_needed

        # Remove the ingredients we just reacted
        ingredient_store[chemical] -= n_runs * reaction.n_out

    # The while loop will terminate once we've satisfied the fuel demand
    return ingredient_store["ORE"]


def react_max_fuel(reactions: Dict[str, Reaction], ore_cargo: int = 10**12) -> int:
    """
    Determine maximum fuel production capability for the provided starting inventory of ORE.

    Since the relationship between ore required to fuel produces is fairly direct, we can shortcut
    from brute force by using the ratio between the current step's ore requirement and the total
    cargo size to increment the fuel guess, adding 1 for the next guess.
    """
    fuel_guess = 1
    # Iterate over fuel guesses until the required ore to react exceeds our ore cargo
    while (ore_required := react_for_fuel(reactions, fuel_guess)) <= ore_cargo:
        # Use max here in case our ratio-based increment puts us over our starting cargo; this is
        # more likely to happen as we approach the cargo capacity
        fuel_guess = max(fuel_guess, (fuel_guess * ore_cargo) // ore_required) + 1

    # Since the loop terminates when we exceed our ore cargo, subtract one to get a reachable state
    return fuel_guess - 1


if __name__ == "__main__":
    puzzle_input = Path("./puzzle_input.txt")

    with puzzle_input.open("r") as f:
        reaction_list = [line.strip() for line in f.readlines()]

    equations = Reaction.from_reaction_list(reaction_list)

    # Part One
    ore_required = react_for_fuel(equations)
    print(ore_required)

    # Part Two
    print(react_max_fuel(equations))
