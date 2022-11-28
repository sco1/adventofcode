import math
from pathlib import Path

import numpy as np

BASE_PATTERN = np.array((0, 1, 0, -1))


def expand_pattern(n_elements: int, element_index: int) -> np.array:  # noqa: D103
    expanded_base = np.repeat(BASE_PATTERN, element_index + 1)

    if expanded_base.size <= n_elements:
        digits_needed = n_elements - expanded_base.size + 1
        tiles_needed = math.ceil(digits_needed / expanded_base.size)
        expanded_base = np.tile(expanded_base, tiles_needed + 1)

    return expanded_base[1 : n_elements + 1]


def parse_signal(signal: str) -> np.array:
    """Parse phase string, assumed to be a string of int, into a 1D Numpy array."""
    return np.array([int(digit) for digit in signal])


def flawft(signal: np.array) -> np.array:
    """
    Apply the Flawed Frequency Transmission (FlawFT) to the provided input signal.

    The FlawFT is calculated by multiplying every value in the input list by a value in a repeating
    pattern and then summing their ones digits.

    The repeating pattern to use depends on which output element is being calculated. The base
    pattern is defined by `base_pattern`: repeat each value in the pattern a number of times equal
    to the position in the output list being considered. The first instance of the initial digit is
    truncated.

    For example:

        Base Pattern: 0, 1, 2
         0th element: 1, 2, 0, 1, 2, ...
         1st element: 0, 1, 1, 2, 2, 0, 0, ...
         2nd element: 0, 0, 1, 1, 1, 2, 2, 2, 0, 0, 0, ...

    See this day's README for a more comprehensive explanation of the transformation applied to each
    phase
    """
    # Stack the signal to create a square matrix
    n_elements = signal.size
    signal_matrix = np.tile(signal, (n_elements, 1))
    pattern_matrix = np.stack([expand_pattern(n_elements, n) for n in range(n_elements)])

    return np.abs((signal_matrix * pattern_matrix).sum(axis=1)) % 10


def run_phases(signal: np.array, n_phases: int) -> str:
    """Run the specified number of flawft phases & emit the first 8 digits of the final signal."""
    for _ in range(n_phases):
        signal = flawft(signal)

    return "".join(str(digit) for digit in signal[:8])


if __name__ == "__main__":
    puzzle_input = Path("./puzzle_input.txt")

    with puzzle_input.open("r") as f:
        raise NotImplementedError
