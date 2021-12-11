from pathlib import Path

import numpy as np
from scipy import ndimage

# Build our left, right, up, and down slices so we can iterate over them
# Assumes we're slicing into an array with a 1-wide padding
SLICES = [
    (slice(1, -1), slice(None, -2)),  # Left
    (slice(1, -1), slice(2, None)),  # Right
    (slice(None, -2), slice(1, -1)),  # Up
    (slice(2, None), slice(1, -1)),  # Down
]


def parse_topography(height_map: list[str]) -> np.ndarray:
    """
    Parse the provided raw height map into an equivalent array.

    The raw height map is assumed to be provided as a list of strings of digits, where each digit
    corresponds to a height reading at the given point. The height map is assumed to be regular and
    no height exceeds 9.
    """
    return np.genfromtxt(height_map, dtype=np.uint8, delimiter=1)


def find_low_points(topo_map: np.ndarray) -> np.ndarray:
    """
    Identify the low points in the provided topographical point.

    Low points are the locations that are lower than any of its adjacent locations. Note that
    diagonals are not considered.
    """
    # Pad with the maximum so we can check around the borders without erroring
    padded = np.pad(topo_map, 1, mode="constant", constant_values=9)
    mask = np.full_like(topo_map, True, dtype=bool)
    for slice_direction in SLICES:
        # For each direction, shift using the equivalent slice & see if the neighbor in that
        # direction is greater than at the (unshifted) query points
        # If we're True in all directions then we have masked out a low point
        mask &= topo_map < padded[slice_direction]

    return topo_map[mask]


def total_risk_level(low_points: np.ndarray) -> int:
    """
    Calculate the total risk level for the provided topographic low points.

    The risk level of a point is calculated as its height plus one.
    """
    return (low_points + 1).sum()


def n_largest_basins(topo_map: np.ndarray, n: int = 3) -> np.ndarray:
    """
    Identify the `n` largest basins in the provided topological map.

    A basin is all locations that eventually flow downward to a single low point. Therefore, every
    low point has a basin, although some basins are very small. Locations of height `9` do not count
    as being in any basin, and all other locations will always be part of exactly one basin.
    """
    # Thank you to: https://stackoverflow.com/a/9441457/2748311
    labeled_map, _ = ndimage.label(topo_map != 9)
    _, basin_size = np.unique(labeled_map[labeled_map != 0], return_counts=True)
    return np.sort(basin_size)[-n:]


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().splitlines()
    topo_map = parse_topography(puzzle_input)

    print(f"Part One: {total_risk_level(find_low_points(topo_map))}")
    print(f"Part Two: {np.prod(n_largest_basins(topo_map))}")
