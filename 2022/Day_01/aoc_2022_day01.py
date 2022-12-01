from collections import abc
from pathlib import Path


def parse_puzzle_input(puzzle_input: str) -> list[int]:
    """
    Parse the provided snack list and calculate the number of calories carried by each elf.

    Elves are assumed to be delimited by a blank line.
    """
    calorie_counts = []
    calorie_sum = 0
    for line in puzzle_input.splitlines():
        if not line:
            calorie_counts.append(calorie_sum)
            calorie_sum = 0
            continue

        calorie_sum += int(line)
    else:
        # Catch any calories from the last line
        if calorie_sum > 0:
            calorie_counts.append(calorie_sum)

    return calorie_counts


def find_most_caloric_dense_elf(calorie_counts: abc.Sequence[int]) -> int:
    """Identify the number of calories carried by the elf with the most snacks."""
    # This could be simpler if we assume the input list is sorted, but will leave generic
    return max(calorie_counts)


def find_best_snack_trio(calorie_counts: abc.Sequence[int]) -> int:
    """Calculate the total calories carried by the three densest elves."""
    calorie_counts = sorted(calorie_counts)
    return sum(calorie_counts[-3:])


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text()

    calorie_counts = parse_puzzle_input(puzzle_input)
    print(f"Part One: {find_most_caloric_dense_elf(calorie_counts)}")
    print(f"Part Two: {find_best_snack_trio(calorie_counts)}")
