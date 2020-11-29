from pathlib import Path
from typing import Tuple

import numpy as np
from scipy import signal


def build_grid(serial: int, width: int = 300, height: int = 300) -> np.ndarray:
    """
    Build a power grid for the given grid serial number
    """
    x, y = np.meshgrid(np.arange(1, width + 1), np.arange(1, height + 1))

    rack_ID = x + 10
    power_level = (rack_ID * y + serial) * rack_ID
    power_level = (power_level // 100) % 10  # Keep hundredths place
    power_level -= 5

    return power_level


def get_max_subgrid_power(power_grid: np.ndarray, subgrid_size: int = 3) -> np.ndarray:
    """
    Use a rolling window to obtain the the power for each subgrid on the power grid

    Assumes power_grid and subgrid(s) are square
    """
    # Use 2d convolution to get the sum of each subgrid
    window = np.ones((subgrid_size, subgrid_size))
    subgrid_powers = signal.convolve2d(
        power_grid, window, mode="valid", boundary="fill", fillvalue=0
    )

    # Map linear index of maximum subgrid power to its coordinates
    j, i = np.unravel_index(subgrid_powers.argmax(), subgrid_powers.shape)
    return (np.amax(subgrid_powers), (i + 1, j + 1))


def part1(serial: int) -> Tuple[int]:
    """
    Find the coordinates of the top left corner of the subgrid with the most power
    """
    power_grid = build_grid(4455)
    max_subgrid_power, subgrid_corner = get_max_subgrid_power(power_grid)

    return subgrid_corner


def part2(serial: int, max_subgrid_size: int = 300) -> Tuple[int]:
    """
    Find the subgrid size that results in the highest total power

    Brute force!
    """
    power_grid = build_grid(4455)

    max_power = 0
    max_power_subgrid_loc = None
    max_power_subgrid_size = 0
    for subgrid_size in range(1, max_subgrid_size + 1):
        max_subgrid_power, subgrid_corner = get_max_subgrid_power(power_grid, subgrid_size)

        if max_subgrid_power > max_power:
            max_power = max_subgrid_power
            max_power_subgrid_loc = subgrid_corner
            max_power_subgrid_size = subgrid_size
    else:
        return max_power_subgrid_loc, max_power_subgrid_size


puzzle_input_file = Path("../../Inputs/puzzle_input_d11.txt")
with puzzle_input_file.open(mode="r") as f:
    serial = int(f.read())

print(part1(serial))
print(part2(serial))
