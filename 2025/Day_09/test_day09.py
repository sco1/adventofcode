import math

from .aoc_2025_day09 import calculate_areas, parse_tiles

SAMPLE_INPUT = """\
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""
TRUTH_TILES = [
    (7, 1),
    (11, 1),
    (11, 7),
    (9, 7),
    (9, 5),
    (2, 5),
    (2, 3),
    (7, 3),
]


def test_parse_tiles() -> None:
    assert parse_tiles(SAMPLE_INPUT) == TRUTH_TILES


def test_calculate_area() -> None:
    areas = calculate_areas(TRUTH_TILES)

    assert len(areas) == math.comb(len(TRUTH_TILES), 2)
    assert areas[0][0] == 50
