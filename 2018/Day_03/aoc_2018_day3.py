import re
from pathlib import Path
from typing import List

import numpy as np


def part1(cloth: np.ndarray) -> int:
    """
    Using the input cloth matrix, find total number of elements > 1, which indicates that claims
    have overlapped
    """
    return np.count_nonzero(cloth > 1)


def part2(cloth: np.ndarray, puzzle_input: List[list]) -> int:
    """
    Iterate over the input cloth matrix and the claims in puzzle_input and find the claim with no
    overlap. This will be where the claim's subarray all equals 1
    """
    for claim in puzzle_input:
        row_indices = (claim[2], (claim[2] + claim[4]))
        column_indices = (claim[1], (claim[1] + claim[3]))

        subarray = cloth[row_indices[0] : row_indices[1], column_indices[0] : column_indices[1]]
        if np.all(subarray == 1):
            return claim[0]


def find_cloth_size(puzzle_input: List[list]) -> tuple:
    """
    Iterate over the claims in puzzle_input and find the coordinates of the bottom right corner of
    the cloth
    """
    max_left = max([claim[1] for claim in puzzle_input])
    max_top = max([claim[2] for claim in puzzle_input])
    max_width = max([claim[3] for claim in puzzle_input])
    max_height = max([claim[4] for claim in puzzle_input])

    return (max_left + max_width), (max_top + max_height)


def build_cloth(puzzle_input: List[list]) -> np.ndarray:
    """
    Iterate over the claims in puzzle_input and add a subarray of ones to the cloth for the cut in
    each claim
    """
    cloth_dims = find_cloth_size(puzzle_input)
    cloth = np.zeros(cloth_dims)

    for claim in puzzle_input:
        row_indices = (claim[2], (claim[2] + claim[4]))
        column_indices = (claim[1], (claim[1] + claim[3]))

        cloth[row_indices[0] : row_indices[1], column_indices[0] : column_indices[1]] += 1

    return cloth


if __name__ == "__main__":
    puzzle_input_file = Path("puzzle_input.txt")
    with puzzle_input_file.open(mode="r") as f:
        """
        Parse the input lines

        Group 1: ID
        Group 2: Left edge
        Group 3: Top edge
        Group 4: Width
        Group 5: Height
        """
        exp = r"#(\d+)\s+@\s+(\d+),(\d+):\s+(\d+)x(\d+)"
        puzzle_input = []
        for claim in f.readlines():
            match = re.match(exp, claim)
            puzzle_input.append([int(param) for param in match.groups()])

    cloth = build_cloth(puzzle_input)

    print(part1(cloth))
    print(part2(cloth, puzzle_input))
