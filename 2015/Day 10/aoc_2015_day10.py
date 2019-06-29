from itertools import groupby
from pathlib import Path
from typing import List


def run_length_endcode(in_str: str) -> List[tuple]:
    """
    Generate the run-length encoding of the input string of single-digit integers as a list of tuple

    e.g. "111221" becomes: [("1", 3), ("2", 2), ("1", 1)]
    """
    return [(digit, sum(1 for i in subgroup)) for digit, subgroup in groupby(in_str)]


def look_and_say(in_str: str, n_iter: int = 40) -> str:
    """
    Play the look-and-say game with the input string of single-digit integers.

    The game is played recursively for a maximum of `n_iter` iterations.
    """
    groupings = run_length_endcode(in_str)
    new_str_components = []
    for group in groupings:
        new_str_components.append(f"{group[1]}{group[0]}")

    new_str = "".join(new_str_components)
    if n_iter > 1:
        return look_and_say(new_str, n_iter - 1)
    else:
        return new_str


puzzle_input_file = Path("./puzzle_input.txt")
with puzzle_input_file.open(mode="r") as f:
    puzzle_input = f.read()

print(len(look_and_say(puzzle_input, 40)))
print(len(look_and_say(puzzle_input, 50)))
