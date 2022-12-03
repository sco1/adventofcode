from functools import cache
from pathlib import Path

import more_itertools as miter


@cache
def _item_priority(item: str) -> int:
    """
    Calculate the item priority.

    Priority is assigned as follows:
        * Lowercase item types `a` through `z` have priorities `1` through `26`
        * Uppercase item types `A` through `Z` have priorities `27` through `52`
    """
    if item.islower():
        return ord(item) - ord("a") + 1
    else:
        return ord(item) - ord("A") + 27


def calculate_overlap_priority(rucksack: str) -> int:
    """
    Calculate the priority of the overlapping item in the provided rucksack's compartments.

    The following assumptions are made:
        * Items are identified by single ASCII letters, where capital and lowercase are distinct
        * The rucksack can be evenly divisible into 2 compartments
        * There is only one overlapping item per rucksack
    """
    if len(rucksack) % 2 != 0:
        raise ValueError(f"Cannot split rucksack into equal compartments. Size: {len(rucksack)}")

    width = len(rucksack) // 2
    left = set(rucksack[:width])
    right = set(rucksack[width:])

    overlap = left & right
    if len(overlap) != 1:
        raise ValueError(f"Did not find exactly one overlap. Found: {len(overlap)}")

    item = overlap.pop()
    return _item_priority(item)


def score_rucksacks(rucksacks: list[str]) -> int:
    """Calculate the total priority score for the provided rucksacks."""
    return sum(calculate_overlap_priority(rucksack) for rucksack in rucksacks)


def score_groups(rucksacks: list[str]) -> int:
    """
    Calculate the total rucksack priority score for each group of 3 elves.

    The following assumptions are made:
        * Items are identified by single ASCII letters, where capital and lowercase are distinct
        * The elves can be evenly grouped into groups of 3
        * There is only one overlapping item per group
    """
    total_priority = 0
    for elf_group in miter.ichunked(rucksacks, 3):
        overlap = set(next(elf_group)).intersection(*elf_group)

        if len(overlap) != 1:
            raise ValueError(f"Did not find exactly one overlap. Found: {len(overlap)}")

        item = overlap.pop()
        total_priority += _item_priority(item)

    return total_priority


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().splitlines()

    print(f"Part One: {score_rucksacks(puzzle_input)}")
    print(f"Part Two: {score_groups(puzzle_input)}")
