import operator
from collections import abc
from pathlib import Path


def max_idx(vals: abc.Iterable[int]) -> tuple[int, int]:
    """Find the maximum value of the provided iterable of `int` and its first index."""
    return max(((b, idx) for idx, b in enumerate(vals)), key=operator.itemgetter(0))


def find_max_joltage(battery_bank: str, select_n: int = 2) -> int:
    """
    Calculate the maximum joltage that can be provided by the specified battery bank.

    Battery banks are assumed to be provided as strings, where each character is the joltage rating,
    a value from `1` to `9`, for its respective battery. For each battery bank, a maximum of
    `select_n` batteries can be turned on to provide the output joltage. The output joltage is equal
    to the number formed by the batteries that have been turned on, e.g. if batteries `2` and `4`
    are turned on, the output joltage is `24`.

    NOTE: Battery banks cannot be rearranged.
    """
    batteries = [int(c) for c in battery_bank]

    # For each battery that we need to turn on, we have to inspect a slice of the entire battery
    # bank for the highest available battery rating; the left boundary is the location of the
    # battery that was just turned on (or the start of the bank for the first round), and the right
    # boundary must be far enough from the end of the bank that we can power on enough batteries by
    # the time we're done iterating.
    left = 0
    joltage = 0
    for i in range(select_n - 1, -1, -1):
        # Can't use negative indexing because it cannot represent the end
        subset = batteries[left : len(batteries) - i]
        max_val, subset_idx = max_idx(subset)

        # Since we're finding the index relative to a subset of batteries, it has to be mapped back
        # to its index in the battery bank; 1 is added so the value we found isn't counted again
        left = subset_idx + left + 1

        # Since we didn't keep battery joltage as a string, we "join" them by math magic
        joltage += max_val * pow(10, i)

    return joltage


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    BATTERY_BANKS = puzzle_input.splitlines()

    print(f"Part One: {sum(find_max_joltage(b) for b in BATTERY_BANKS)}")
    print(f"Part Two: {sum(find_max_joltage(b, select_n=12) for b in BATTERY_BANKS)}")
