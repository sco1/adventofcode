import itertools
from pathlib import Path


def Day2a(puzzle_input: list[str]) -> int:
    """
    Calculate the checksum for the provided spreadsheet.

    For each row, determine the difference between the largest value and the smallest value; the
    checksum is the sum of all of these differences.

    For example, given the following spreadsheet:

    5 1 9 5
    7 5 3
    2 4 6 8

    * The first row's largest and smallest values are 9 and 1, and their difference is 8.
    * The second row's largest and smallest values are 7 and 3, and their difference is 4.
    * The third row's difference is 6.

    In this example, the spreadsheet's checksum would be 8 + 4 + 6 = 18.
    """
    m = readtxt(puzzle_input)

    output = 0
    for row in m:
        rowmin = min(row)
        rowmax = max(row)
        drow = rowmax - rowmin

        output += drow

    return output


def Day2b(puzzle_input: list[str]) -> int:
    """
    Calculate the checksum for the provided spreadsheet using the alternative algorithm.

    It sounds like the goal is to find the only two numbers in each row where one evenly divides the
    other - that is, where the result of the division operation is a whole number. They would like
    you to find those numbers on each line, divide them, and add up each line's result.

    For example, given the following spreadsheet:

    5 9 2 8
    9 4 7 3
    3 8 6 5

    * In the first row, the only two numbers that evenly divide are 8 and 2; the result of this
    division is 4.
    * In the second row, the two numbers are 9 and 3; the result is 3.
    * In the third row, the result is 2.

    In this example, the sum of the results would be 4 + 3 + 2 = 9.
    """
    m = readtxt(puzzle_input)

    output = 0
    for row in m:
        # Time for some brute force!
        for pair in itertools.combinations(row, 2):
            test = max(pair) % min(pair)
            if test == 0:
                output += max(pair) // min(pair)
                break

    return output


def readtxt(puzzle_input: list[str]) -> list[list[int]]:
    """Read in puzzle input."""
    m = []
    for line in puzzle_input:
        m.append([int(x) for x in line.split()])

    return m


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().splitlines()

    print(f"Part One: {Day2a(puzzle_input)}")
    print(f"Part Two: {Day2b(puzzle_input)}")
