from pathlib import Path

import numpy as np
from scipy import signal

# The sliding window we'll use with the 2D convolution to flash energy into neighboring octopi
WINDOW = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]], dtype=np.uint8)


def parse_energy_levels(energy_reading: list[str]) -> np.ndarray:
    """
    Parse the energy readings into an equivalent array.

    The raw energy reading is assumed to be provided as a list of strings of digits, where each
    digit the energy of a Dumbo Octopus swimming at the specified coordinates. The grid is assumed
    to be regular and no energy level exceeds 9.
    """
    return np.genfromtxt(energy_reading, dtype=np.uint8, delimiter=1)


def _step_dumbo_cave(energy: np.ndarray) -> int:
    """
    Calculate the number of Dumbo Octopus flashes that occur while incrementing the time step.

    For each time step:
        * The energy level of each octopus increases by 1
        * Any octopus with an energy greater than 9 flashes. When an octopus flashes, the energy
        level of each neighboring octopus is increased by 1, then the flashing octopus' energy level
        drops to 0.
        * The flashing process continues until no new octopi have their energy level increased above
        9.
        * An octopus can only flash once per time step
    """
    energy += 1

    # Keep track of which octopi have already flashed, they can only do this once per step
    flashed_mask = np.zeros_like(energy, dtype=bool)
    while np.any(is_flashing := (~flashed_mask & (energy > 9))):
        # The 2D convolution of the flashing mask and our sliding window gives the number of
        # neighbors that are going to flash, which will each add one to the octopus in the center
        # Continue cycling through until no new octopi have flashed
        energy += signal.convolve2d(is_flashing, WINDOW, mode="same")
        flashed_mask |= is_flashing  # Mark the flashed octopi

    energy[energy > 9] = 0  # Reset all of the flashed octopi
    return np.sum(flashed_mask)


def model_dumbo_cave(starting_energy: np.ndarray, n_steps: int) -> int:
    """Step through our Dumbo Octopus Cave Simulation (DOCS) for the specified number of steps."""
    return sum(_step_dumbo_cave(starting_energy) for _ in range(n_steps))


def find_first_sync(starting_energy: np.ndarray) -> int:
    """Run the DOCS until we encounter a time step where all octopi flash simultaneously."""
    step = 1
    target = np.prod(starting_energy.shape)
    while True:
        if _step_dumbo_cave(starting_energy) == target:
            return step

        step += 1


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().splitlines()

    starting_energy = parse_energy_levels(puzzle_input)
    print(f"Part One: {model_dumbo_cave(starting_energy, 100)}")

    starting_energy = parse_energy_levels(puzzle_input)  # reparse since we mutated in place
    print(f"Part Two: {find_first_sync(starting_energy)}")
