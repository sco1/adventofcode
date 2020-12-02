import re
from collections import abc
from pathlib import Path


def parse_input(puzzle_input: list[str]) -> tuple[dict[str, list[str]], str]:
    """
    Parse the provided puzzle input into a container of reactions & the starting molecule.

    Puzzle input is expected to be the `str.splitlines()` output from the following:
        H => HO
        H => OH
        O => HH

        HOH

    Where the input starts with a series of reactions, followed by a blank space, followed by the
    starting molecule.
    """
    reactions = {}
    starting_molecule = ""
    for line in puzzle_input:
        if not line:
            # Delimiter
            continue

        if "=>" in line:
            # Reaction
            reactant, _, product = line.partition("=>")

            # To make iterating simpler later, store a list of possible products for each reactant
            # Use setdefault to make a clever one-liner
            reactions.setdefault(reactant.strip(), []).append(product.strip())
        else:
            # Arrived at starting molecule
            starting_molecule = line

    return reactions, starting_molecule


def count_unique_products(reactions: dict[str, list[str]], base_molecule: str) -> int:
    """Count the number of unique molecules generated in one step from the provided reactions."""
    return len(set(make_reaction(reactions, base_molecule)))


def make_reaction(reactions: dict[str, list[str]], base_molecule: str) -> abc.Iterator[str]:
    """"""
    # Split into atoms so we're not iterating over individual letters
    # Assume any possible atom is a capital letter followed by either 0 or 1 lowercase letters
    atoms = re.findall(r"[A-Z][a-z]?", base_molecule)
    for idx, atom in enumerate(atoms):
        for product in reactions.get(atom, []):
            yield "".join(atoms[:idx] + [product] + atoms[(idx + 1) :])  # noqa: E203 black bug


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().splitlines()

    reactions, starting_molecule = parse_input(puzzle_input)
    print(f"Part 1: {count_unique_products(reactions, starting_molecule)} unique combinations")
