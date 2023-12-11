import itertools
from collections import abc
from pathlib import Path

from helpers.geometry import BoundingBox, COORD, manhattan_distance
from helpers.parsing import parse_hashed_map


def parse_galaxy_map(galaxy_map: str, scale_factor: int = 2) -> set[COORD]:
    """
    Parse the provided 2D galactic map and provide coordinates for all noted galaxy locations.

    To account for the expansion of the Universe, a scaling factor is used to map the expansion
    during creation of the map. Each empty row and column of the provided map are expanded using the
    specified factor before coordinates are generated. e.g. with a `scale_factor` of `2` (the
    default), each empty row/column is doubled in size.
    """
    galaxy_coords = parse_hashed_map(galaxy_map)
    raw_x = {x for x, _ in galaxy_coords}
    raw_y = {y for _, y in galaxy_coords}

    # Identify any rows and columns that don't contain any galaxies & expand them, updating affected
    # coordinates as they expand
    drawn_bbox = BoundingBox(galaxy_coords)
    empty_rows = []
    for y in drawn_bbox.y_bound:
        if y not in raw_y:
            empty_rows.append(y)

    empty_cols = []
    for x in drawn_bbox.x_bound:
        if x not in raw_x:
            empty_cols.append(x)

    shifted_coords = set()
    for x, y in galaxy_coords:
        n_x = x + sum(x > col for col in empty_cols) * (scale_factor - 1)
        n_y = y + sum(y > row for row in empty_rows) * (scale_factor - 1)

        shifted_coords.add((n_x, n_y))

    return shifted_coords


def galaxy_dist(origin: COORD, destination: COORD) -> int:
    """Calculate the intergalactic Manhattan Distance between a pair of galactic coordinates."""
    return manhattan_distance(origin, destination)


def sum_galaxy_pdist(galaxy_coords: abc.Iterable[COORD]) -> int:
    """Calculate the sum of all pairwise distances of the provided galaxy coordinates."""
    return sum(galaxy_dist(*pair) for pair in itertools.combinations(galaxy_coords, 2))


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    galaxy_coords = parse_galaxy_map(puzzle_input)
    print(f"Part One: {sum_galaxy_pdist(galaxy_coords)}")

    galaxy_coords = parse_galaxy_map(puzzle_input, scale_factor=1_000_000)
    print(f"Part Two: {sum_galaxy_pdist(galaxy_coords)}")
