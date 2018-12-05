from pathlib import Path


def part1(puzzle_input: list) -> int:
    return sum(puzzle_input)


def part2(puzzle_input: list) -> int:
    frequency = 0
    frequency_steps = set([frequency])

    while True:
        for frequency_shift in puzzle_input:
            frequency += frequency_shift
            if frequency in frequency_steps:
                return frequency
            else:
                frequency_steps.add(frequency)


puzzle_input_file = Path("../../Inputs/puzzle_input_d1.txt")
with puzzle_input_file.open(mode="r") as f:
    puzzle_input = f.readlines()

puzzle_input = [int(freq) for freq in puzzle_input]

print(part1(puzzle_input))
print(part2(puzzle_input))
