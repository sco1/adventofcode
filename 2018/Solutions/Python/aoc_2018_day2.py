from collections import Counter
from math import floor
from pathlib import Path

from fuzzywuzzy import process


def part1(puzzle_input: list) -> int:
    counted_input = [Counter(container) for container in puzzle_input]

    n_doubles = 0
    n_triples = 0
    for container in counted_input:
        if 2 in container.values():
            n_doubles += 1

        if 3 in container.values():
            n_triples += 1

    return n_doubles * n_triples


def part2(puzzle_input: list) -> str:
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


puzzle_input_file = Path("../../.inputs/puzzle_input_d2.txt")
with puzzle_input_file.open(mode="r") as f:
    puzzle_input = f.readlines()

puzzle_input = [line.strip() for line in puzzle_input]

print(part1(puzzle_input))
print(part2(puzzle_input))
