import re
from pathlib import Path

import numpy as np


def starfield_params(star_position: np.ndarray) -> int:
    """
    Calculate starfield bounding box dimensions & area
    """
    xmin = min(star_position[:, 0])
    xmax = max(star_position[:, 0])
    ymin = min(star_position[:, 1])
    ymax = max(star_position[:, 1])

    width = xmax - xmin
    height = ymax - ymin
    area = width * height

    return area, width, height, xmin, xmax, ymin, ymax


def star_message(star_position: np.ndarray, star_velocity: np.ndarray) -> str:
    """
    Find the message in the stars!

    Attempt to find the message by finding where the total star area is minimized
    """
    last_area = None
    elapsed_seconds = 0
    while True:
        # Calculate the area of the current star position bounding box
        area = starfield_params(star_position)

        if last_area and area > last_area:
            # We should be one timestamp step past the message
            star_position -= star_velocity
            elapsed_seconds -= 1

            # Build display string
            _, width, height, xmin, _, ymin, _ = starfield_params(star_position)
            message = np.zeros((height + 1, width + 1), dtype=str)
            message[:] = "."
            idx = star_position.T
            message[idx[1, :] - ymin, idx[0, :] - xmin] = "#"  # Normalize the message

            return message, elapsed_seconds
        else:
            last_area = area
            star_position += star_velocity
            elapsed_seconds += 1


puzzle_input_file = Path("../../Inputs/puzzle_input_d10.txt")
with puzzle_input_file.open(mode="r") as f:
    exp = r"(-?\d+)"
    puzzle_input = []
    for line in f:
        x, y, dx, dy = map(int, re.findall(exp, line))
        puzzle_input.append(([x, y], (dx, dy)))

star_position = np.array([star[0] for star in puzzle_input])
star_velocity = np.array([star[1] for star in puzzle_input])
message, time_elapsed = star_message(star_position, star_velocity)

[print("".join(row)) for row in message.tolist()]
print(time_elapsed)
