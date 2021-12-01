from pathlib import Path

import more_itertools as mi


def count_adjacent(soundings: list[int]) -> int:
    """Count the number of times the depth sounding increases from the previous measurement."""
    n_ascending = 0
    for left, right in mi.sliding_window(soundings, 2):
        if right > left:
            n_ascending += 1

    return n_ascending


def count_sums(soundings: list[int], width: int = 3) -> int:
    """Count the number of times the sum of a sliding window increases from the previous."""
    last_sum = None
    n_ascending = 0
    for window in mi.sliding_window(soundings, width):
        current_sum = sum(window)
        if last_sum is not None:  # Skip first iteration
            if current_sum > last_sum:
                n_ascending += 1

        last_sum = current_sum

    return n_ascending


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = [int(line) for line in puzzle_input_file.read_text().splitlines()]

    n_ascending_1 = count_adjacent(puzzle_input, 2)
    print(f"Part One: {n_ascending_1}")

    n_ascending_2 = count_sums(puzzle_input, 3)
    print(f"Part Two: {n_ascending_2}")
