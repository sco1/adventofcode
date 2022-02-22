import operator
import typing as t
from pathlib import Path
from textwrap import dedent

GIFT_CLUE = dedent(
    """\
    children: 3
    cats: 7
    samoyeds: 2
    pomeranians: 3
    akitas: 0
    vizslas: 0
    goldfish: 5
    trees: 3
    cars: 2
    perfumes: 1
    """
).splitlines()


def parse_gift_clue(clue_input: list[str]) -> dict[str, int]:
    """
    Remap the provided gift clue into a dictionary.

    Clues are assumed to be given as <item>:<quantity> key, value pairs
    """
    return {gift: int(quantity) for line in clue_input for gift, quantity in (line.split(":"),)}


def parse_aunts(puzzle_input: list[str]) -> dict[str, dict[str, int]]:
    """
    Parse the provided puzzle input an aunt gift mapping.

    Aunt specification comes in the form:
        "Sue 1: children: 1, cars: 8, vizslas: 7"
    """
    aunts_map = {}
    for line in puzzle_input:
        aunt, _, items = line.partition(":")
        aunt = aunt.strip()
        aunts_map[aunt] = {}
        for subgift in items.split(","):
            gift, _, quantity = subgift.partition(":")
            aunts_map[aunt][gift.strip()] = int(quantity)

    return aunts_map


def find_aunt(
    aunts_map: dict[str, dict[str, int]],
    gift_clue: dict[str, int],
    ops_override: dict[str, t.Callable] = {},  # noqa: B006
) -> str:
    """
    Match the provided gift clue to the aunt that sent the gift.

    Ops may be optionally specified to use operators other than equality for comparison of specific
    items. For example, we can specify `ops={"cats": operator.gt}` to indicate that the aunt needs
    to have more than the provided number of cats.
    """
    for aunt, inventory_memory in aunts_map.items():
        # Since our memory of our aunt's inventory is hazy, we first check that the item from the
        # clue is present in what we remember, and if it is then we can check the quantity
        for item, aunt_quantity in inventory_memory.items():
            # Check for a custom comparison, otherwise default to equality
            op = ops_override.get(item, operator.eq)
            if not op(aunt_quantity, gift_clue[item]):
                break
        else:
            return aunt


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().splitlines()

    gift_clue = parse_gift_clue(GIFT_CLUE)
    aunts = parse_aunts(puzzle_input)

    print(f"Part One: {find_aunt(aunts, gift_clue)}")

    ops = {
        "cats": operator.gt,
        "trees": operator.gt,
        "pomeranians": operator.lt,
        "goldfish": operator.lt,
    }

    print(f"Part Two: {find_aunt(aunts, gift_clue, ops)}")
