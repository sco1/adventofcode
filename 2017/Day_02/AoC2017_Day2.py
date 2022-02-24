import itertools
from pathlib import Path


def checksum_minmax(spreadsheet: list[list[int]]) -> int:
    """
    Calculate the checksum for the provided spreadsheet.

    The checksum is calculated by summing the difference between the min and max for each row.
    """
    checksum = sum((max(row) - min(row)) for row in spreadsheet)

    return checksum


def checksum_divisible(spreadsheet: list[list[int]]) -> int:
    """
    Calculate the checksum for the provided spreadsheet.

    The checksum is calculated by summing the difference between the two numbers on each line who
    are evenly divisible. It is assumed that there is only one pair of such numbers in each row.
    """
    checksum = 0
    for row in spreadsheet:
        for pair in itertools.combinations(row, 2):
            # Divide the max by the min since the other way around will never give a whole number
            # unless they're the same
            res, mod = divmod(max(pair), min(pair))
            if mod == 0:
                checksum += res
                break  # Assuming only one satisfactory pair in each row

    return checksum


def parse_spreadsheet(puzzle_input: list[str]) -> list[list[int]]:
    """Read in puzzle input."""
    m = []
    for line in puzzle_input:
        m.append([int(x) for x in line.split()])

    return m


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().splitlines()
    spreadsheet = parse_spreadsheet(puzzle_input)

    print(f"Part One: {checksum_minmax(spreadsheet)}")
    print(f"Part Two: {checksum_divisible(spreadsheet)}")
