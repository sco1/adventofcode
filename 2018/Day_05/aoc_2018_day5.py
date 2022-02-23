from pathlib import Path
from string import ascii_lowercase, ascii_uppercase
from typing import List


def build_pairs() -> List[str]:
    """
    Return a list of pairs of caseswapped ASCII characters
    """
    out = [f"{letter}{letter.upper()}" for letter in ascii_lowercase]
    out += [pair.swapcase() for pair in out]

    return out


def part1(puzzle_input: str) -> int:
    reacting_pairs = build_pairs()

    n_units = len(puzzle_input)
    while True:
        for pair in reacting_pairs:
            puzzle_input = puzzle_input.replace(pair, "")

        # Break out if nothing has changed, meaning all of the reactions are complete
        reacted_length = len(puzzle_input)
        if reacted_length == n_units:
            break
        else:
            n_units = reacted_length

    return reacted_length


def part2(puzzle_input: str):
    # Swap out each letter & rerun part 1 to see which is the best to remove
    return min(
        [
            part1(puzzle_input.replace(lletter, "").replace(uletter, ""))
            for lletter, uletter in zip(ascii_lowercase, ascii_uppercase)
        ]
    )


if __name__ == "__main__":
    puzzle_input_file = Path("puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    print(part1(puzzle_input))
    print(part2(puzzle_input))
