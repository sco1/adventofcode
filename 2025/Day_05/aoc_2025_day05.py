import typing as t
from collections import abc
from pathlib import Path

RANGE_T: t.TypeAlias = tuple[int, int]


def parse_database(database_copy: str) -> tuple[list[RANGE_T], list[int]]:
    """
    Parse the provided inventory management database copy into its components.

    The database copy is assumed to consist of two components, the fresh ingredient ID ranges and
    available ingredient IDs, delimited by a blank line. ID ranges are assumed to be newline
    delimited and of the form `<left>-<right>` where `left` and `right` are specified as integers;
    ranges are inclusive. Ingredient IDs are assumed to be newline delimited integers.

    NOTE: To assist with downstream tasks, parsed ID ranges are returned in sorted order.
    """
    raw_ranges, raw_ingredients = database_copy.split("\n\n")

    fresh_ranges = []
    for rr in raw_ranges.splitlines():
        left, right = rr.split("-")

        # Store ranges as ints to avoid overhead of range
        fresh_ranges.append((int(left), int(right)))

    available_ingredients = [int(n) for n in raw_ingredients.splitlines()]

    # Sort the ranges to help with part 2
    return sorted(fresh_ranges), available_ingredients


def is_fresh(fresh_ranges: abc.Iterable[RANGE_T], ingredient_id: int) -> bool:
    """
    Determine if the query ID is contained by any of the provided fresh ingredient ID ranges.

    NOTE: Ingredient ID ranges are inclusive.
    """
    if any((s <= ingredient_id <= e) for s, e in fresh_ranges):
        return True
    else:
        return False


def n_fresh(fresh_ranges: abc.Iterable[RANGE_T], ingredients: abc.Iterable[int]) -> int:
    """Determine the number of fresh ingredients in the inventory management system."""
    return sum(is_fresh(fresh_ranges, i) for i in ingredients)


def collapse_ranges(fresh_ranges: abc.Iterable[RANGE_T]) -> int:
    """
    Determine the total number of ingredient IDs represented by the provided ID ranges.

    NOTE: ID ranges are assumed to already be sorted.
    """
    n_ids = 0
    curr = 0  # Keep track of the rightmost number we encounter as we iterate through the ranges
    for left, right in fresh_ranges:
        # Check if we have already partially counted IDs in the current range
        if curr >= left:
            left = curr + 1  # Current place has already been counted

        if left <= right:
            n_ids += (right - left) + 1

        curr = max(curr, right)  # Make sure we don't go backwards

    return n_ids


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    fresh_ranges, ingredients = parse_database(puzzle_input)

    print(f"Part One: {n_fresh(fresh_ranges, ingredients)}")
    print(f"Part Two: {collapse_ranges(fresh_ranges)}")
