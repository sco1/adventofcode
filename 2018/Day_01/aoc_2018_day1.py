from pathlib import Path


def part1(puzzle_input: list[int]) -> int:
    return sum(puzzle_input)


def part2(puzzle_input: list[int]) -> int:
    frequency = 0
    frequency_steps = set([frequency])

    while True:
        for frequency_shift in puzzle_input:
            frequency += frequency_shift
            if frequency in frequency_steps:
                return frequency
            else:
                frequency_steps.add(frequency)


if __name__ == "__main__":
    puzzle_input_file = Path("puzzle_input.txt")
    puzzle_input = [int(freq) for freq in puzzle_input_file.read_text().splitlines()]

    print(part1(puzzle_input))
    print(part2(puzzle_input))
