from pathlib import Path


def part1(frequency_changes: list[int]) -> int:
    """Determine the resulting frequency after applying the provided frequency changes."""
    return sum(frequency_changes)


def part2(frequency_changes: list[int]) -> int:
    """Identify the first repeat frequency while applying the provided frequency changes."""
    frequency = 0
    seen = set([frequency])

    while True:
        for shift in frequency_changes:
            frequency += shift
            if frequency in seen:
                return frequency
            else:
                seen.add(frequency)


if __name__ == "__main__":
    puzzle_input_file = Path("puzzle_input.txt")
    puzzle_input = [int(freq) for freq in puzzle_input_file.read_text().splitlines()]

    print(f"Part One: {part1(puzzle_input)}")
    print(f"Part Two: {part2(puzzle_input)}")
