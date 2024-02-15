import re
from pathlib import Path
from typing import List

import numpy as np


class LightGrid:
    """Represents a grid of holiday lights!"""

    def __init__(self, length: int = 1000, width: int = 1000) -> None:
        """Initialize the grid of holiday lights based on the given dimensions."""
        self.length = length
        self.width = width

    def process_instructions(self, instruction_set: List[str]) -> None:
        """Process the lighting instructions, provided as a list of strings."""
        coord_exp = r"(\d+,\d+)"  # Regex pattern to extract coordinate pairs
        for instruction in instruction_set:
            instruction = instruction.lower()  # Normalize the instruction

            # Extract the corner coordinates into separate lists
            # Assumes each instruction has 2 pairs of coordinates
            raw_coord_pairs = re.findall(coord_exp, instruction)
            top_left, bottom_right = [
                [int(num) for num in pair.split(",")] for pair in raw_coord_pairs
            ]

            # Process the instruction
            if instruction.startswith("turn on"):
                self.lights_on(top_left, bottom_right)
            elif instruction.startswith("turn off"):
                self.lights_off(top_left, bottom_right)
            elif instruction.startswith("toggle"):
                self.lights_toggle(top_left, bottom_right)
            else:
                raise ValueError(f"Unknown instruction: '{instruction}'")

    def n_lit_lights(self) -> int:
        """Return the number of lights in the grid that are turned on."""
        return np.count_nonzero(self.light_grid)


class OnOffGrid(LightGrid):
    """Represents a light grid where lights only have on/off state."""

    def __init__(self, length: int = 1000, width: int = 1000):
        super().__init__(length=length, width=width)
        self.light_grid = np.zeros((self.length, self.width), dtype=bool)  # All lights start off

    def lights_on(self, top_left: List[int], bottom_right: List[int]) -> None:
        """
        Turn the lights in the grid specified by the input corner coordinate pairs.

        Numpy indexing is (row, column) and coordinates are provided as (column, row)
        """
        self.light_grid[top_left[1] : bottom_right[1] + 1, top_left[0] : bottom_right[0] + 1] = True

    def lights_off(self, top_left: List[int], bottom_right: List[int]) -> None:
        """
        Turn off the lights in the grid specified by the input corner coordinate pairs.

        Numpy indexing is (row, column) and coordinates are provided as (column, row)
        """
        self.light_grid[top_left[1] : bottom_right[1] + 1, top_left[0] : bottom_right[0] + 1] = (
            False
        )

    def lights_toggle(self, top_left: List[int], bottom_right: List[int]) -> None:
        """
        Toggle the lights in the grid specified by the input corner coordinate pairs.

        Numpy indexing is (row, column) and coordinates are provided as (column, row)
        """
        # Split coordinates to save typing
        y1, x1 = top_left
        y2, x2 = bottom_right
        self.light_grid[x1 : x2 + 1, y1 : y2 + 1] = ~self.light_grid[x1 : x2 + 1, y1 : y2 + 1]


class BrightnessGrid(LightGrid):
    """Represents a light grid where lights have a brightness."""

    def __init__(self, length: int = 1000, width: int = 1000):
        super().__init__(length=length, width=width)
        self.light_grid = np.zeros((self.length, self.width), dtype=int)  # All lights start off

    def lights_on(self, top_left: List[int], bottom_right: List[int]) -> None:
        """
        Increase light brightness by 1 in the grid specified by the input corner coordinate pairs.

        Numpy indexing is (row, column) and coordinates are provided as (column, row)
        """
        self.light_grid[top_left[1] : bottom_right[1] + 1, top_left[0] : bottom_right[0] + 1] += 1

    def lights_off(self, top_left: List[int], bottom_right: List[int]) -> None:
        """
        Decrease light brightness by 1 in the grid specified by the input corner coordinate pairs.

        Negative numbers are reset to 0

        Numpy indexing is (row, column) and coordinates are provided as (column, row)
        """
        self.light_grid[top_left[1] : bottom_right[1] + 1, top_left[0] : bottom_right[0] + 1] -= 1

        # Reset any negative values to 0
        mask = (
            self.light_grid[top_left[1] : bottom_right[1] + 1, top_left[0] : bottom_right[0] + 1]
            < 0
        )
        self.light_grid[
            top_left[1] : bottom_right[1] + 1, top_left[0] : bottom_right[0] + 1
        ] *= ~mask

    def lights_toggle(self, top_left: List[int], bottom_right: List[int]) -> None:
        """
        Increase light brightness by 2 in the grid specified by the input corner coordinate pairs.

        Numpy indexing is (row, column) and coordinates are provided as (column, row)
        """
        self.light_grid[top_left[1] : bottom_right[1] + 1, top_left[0] : bottom_right[0] + 1] += 2

    def total_brightness(self) -> None:
        """Return the total brightness of the grid."""
        return np.sum(self.light_grid)


puzzle_input_file = Path("./puzzle_input.txt")
with puzzle_input_file.open(mode="r") as f:
    puzzle_input = f.readlines()

holiday_lights = OnOffGrid()
holiday_lights.process_instructions(puzzle_input)
print(holiday_lights.n_lit_lights())

bright_holiday_lights = BrightnessGrid()
bright_holiday_lights.process_instructions(puzzle_input)
print(bright_holiday_lights.total_brightness())
