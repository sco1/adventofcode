from collections import Counter
from math import floor
from pathlib import Path

from rapidfuzz import process


def part1(puzzle_input: list[str]) -> int:
    counted_input = [Counter(container) for container in puzzle_input]

    n_doubles = 0
    n_triples = 0
    for container in counted_input:
        if 2 in container.values():
            n_doubles += 1

        if 3 in container.values():
            n_triples += 1

    return n_doubles * n_triples


def part2(puzzle_input: list[str]) -> str:
    for teststr in puzzle_input:
        # Get closest match, ignore self match
        test = process.extract(teststr, puzzle_input, limit=2)[1]

        # Match should differ by 1 character, calculate this percentage and use as a threshold
        diff_threshold = floor(((len(teststr) - 1) / len(teststr)) * 100)

        if test[1] >= diff_threshold:
            a = list(test[0])
            b = list(teststr)

            for idx, letter in enumerate(a):
                if b[idx] != letter:
                    b.pop(idx)
                    return "".join(b)


if __name__ == "__main__":
    puzzle_input_file = Path("puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().splitlines()

    print(part1(puzzle_input))
    print(part2(puzzle_input))
