import itertools
from collections import abc
from pathlib import Path

from helpers.geometry import COORD


def parse_tiles(tile_map: str) -> list[COORD]:
    """
    Parse the provided theater tile map into its specified red tile locations.

    Locations of the red tiles in the theater are assumed to be provided as newline-delimited
    coordinates of `X,Y` integers.
    """
    red_tiles = []
    for line in tile_map.splitlines():
        raw_x, raw_y = line.split(",")
        red_tiles.append((int(raw_x), int(raw_y)))

    return red_tiles


def calculate_areas(available_tiles: abc.Iterable[COORD]) -> list[tuple[int, COORD, COORD]]:
    """Calculate all possible rectangular areas formed by pairs of red tile locations."""
    areas = []
    for (a_x, a_y), (b_x, b_y) in itertools.combinations(available_tiles, 2):
        # Assume tiles are unit height & add one so we don't incorrectly get zero area
        area = (abs(a_x - b_x) + 1) * (abs(a_y - b_y) + 1)
        areas.append((area, (a_x, a_y), (b_x, b_y)))

    areas.sort(reverse=True)
    return areas


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    red_tiles = parse_tiles(puzzle_input)

    areas = calculate_areas(red_tiles)
    print(f"Part One: {areas[0][0]}")
    print(f"Part Two: {...}")
