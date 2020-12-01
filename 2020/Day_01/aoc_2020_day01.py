from math import prod
from pathlib import Path

import more_itertools as mi


def find_sum_combo(
    entries: list[int], target: int = 2020, n_entries: int = 2
) -> tuple[int, tuple[int]]:
    """
    Iterate through the provided entries & identify the grouping that sums to the target value.

    The product of the grouping is returned, along with the entry group.
    """
    for group in mi.distinct_combinations(entries, n_entries):
        if sum(group) == target:
            return prod(group), group


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = [int(line) for line in puzzle_input_file.read_text().splitlines()]

    expense_product_pair, entry_pair = find_sum_combo(puzzle_input)
    print(f"Part One: {expense_product_pair}")

    expense_product_trio, entry_trio = find_sum_combo(puzzle_input, n_entries=3)
    print(f"Part Two: {expense_product_trio}")
