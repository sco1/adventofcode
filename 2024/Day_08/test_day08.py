from textwrap import dedent

from helpers.geometry import BoundingBox, COORD
from .aoc_2024_day08 import find_antinodes, parse_antenna_map

SAMPLE_INPUT = dedent(
    """\
    ............
    ........0...
    .....0......
    .......0....
    ....0.......
    ......A.....
    ............
    ............
    ........A...
    .........A..
    ............
    ............
    """
)

TRUTH_ANTENNAS = {
    "0": {(4, 4), (5, 2), (7, 3), (8, 1)},
    "A": {(6, 5), (8, 8), (9, 9)},
}
TRUTH_BBOX = BoundingBox(((0, 0), (0, 11), (11, 0), (11, 11)))


def test_map_parse() -> None:
    antenna_locations, map_bbox = parse_antenna_map(SAMPLE_INPUT)
    assert antenna_locations == TRUTH_ANTENNAS
    assert map_bbox == TRUTH_BBOX


TRUTH_ANTINODES = {
    "0": {(0, 7), (6, 5), (1, 5), (3, 1), (11, 0), (2, 3), (3, 6), (6, 0), (10, 2), (9, 4)},
    "A": {(10, 11), (7, 7), (3, 1), (4, 2), (10, 10)},
}


def test_find_antinodes() -> None:
    antenna_locations, map_bbox = parse_antenna_map(SAMPLE_INPUT)
    antinodes = find_antinodes(antenna_locations, map_bbox)
    assert antinodes == TRUTH_ANTINODES

    unique_antinodes: set[COORD] = set()
    unique_antinodes.update(*antinodes.values())
    assert len(unique_antinodes) == 14


def test_find_antinodes_with_resonance() -> None:
    antenna_locations, map_bbox = parse_antenna_map(SAMPLE_INPUT)
    antinodes = find_antinodes(antenna_locations, map_bbox, add_resonant=True)

    for freq, anti in antinodes.items():
        print(freq)
        print(sorted(anti))

    unique_antinodes: set[COORD] = set()
    unique_antinodes.update(*antinodes.values())
    assert len(unique_antinodes) == 34
