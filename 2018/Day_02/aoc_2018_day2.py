from collections import Counter
from math import floor
from pathlib import Path

from rapidfuzz import process


def part1(container_ids: list[str]) -> int:
    """
    Calculate the checksum of the provided inventory box IDs.

    The checksum is determined by multiplying the number of IDs containing exactly two of any letter
    by the number of IDs containing exactly three of any letter.

    NOTE: If there are more than one two-char or three-char repeats in a given container ID, it is
    only counted once.
    """
    id_char_counts = [Counter(container) for container in container_ids]

    n_doubles = 0
    n_triples = 0
    for container in id_char_counts:
        if 2 in container.values():
            n_doubles += 1

        if 3 in container.values():
            n_triples += 1

    return n_doubles * n_triples


def part2(container_ids: list[str]) -> str:
    """
    Identify the the boxes full of prototype fabric.

    The boxes will have IDs which differ by exactly one character at the same position in both
    strings. The letters common between the two correct box IDs are returned.
    """
    for container in container_ids:
        # Get closest match, ignore self match
        test = process.extract(container, container_ids, limit=2)[1]

        # Match should differ by 1 character, calculate this percentage and use as a threshold
        diff_threshold = floor(((len(container) - 1) / len(container)) * 100)

        if test[1] >= diff_threshold:
            a = list(test[0])
            b = list(container)

            for idx, letter in enumerate(a):
                if b[idx] != letter:
                    b.pop(idx)
                    return "".join(b)

    raise ValueError("Could not locate a valid pair of boxes.")


if __name__ == "__main__":
    puzzle_input_file = Path("puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().splitlines()

    print(f"Part One: {part1(puzzle_input)}")
    print(f"Part Two: {part2(puzzle_input)}")
