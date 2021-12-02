from pathlib import Path

import more_itertools as mi


def count_ascending(soundings: list[int], width: int = 1) -> int:
    """
    Count the number of times the sum of a sliding window increases from the previous window.

    A window width of 1 can be used to consider adjacent values.
    """
    n_ascending = 0
    # When comparing the sums of adjacent sliding windows, they share the middle value(s) so the
    # only delta we need to consider is between the valuies on the boundary of their combined window
    for left, *_, right in mi.sliding_window(soundings, width + 1):
        if right > left:
            n_ascending += 1

    return n_ascending


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = [int(line) for line in puzzle_input_file.read_text().splitlines()]

    n_ascending_1 = count_ascending(puzzle_input, 1)
    print(f"Part One: {n_ascending_1}")

    n_ascending_2 = count_ascending(puzzle_input, 3)
    print(f"Part Two: {n_ascending_2}")
