from textwrap import dedent

import pytest

from helpers.geometry import COORD
from .aoc_2023_day11 import galaxy_dist, parse_galaxy_map, sum_galaxy_pdist

SAMPLE_INPUT = dedent(
    """\
    ...#......
    .......#..
    #.........
    ..........
    ......#...
    .#........
    .........#
    ..........
    .......#..
    #...#.....
    """
)

TRUTH_EXPANDED = dedent(
    """\
    ....1........
    .........2...
    3............
    .............
    .............
    ........4....
    .5...........
    ............6
    .............
    .............
    .........7...
    8....9.......
    """
)
TRUTH_COORDS = set()
for y, line in enumerate(TRUTH_EXPANDED.splitlines()):
    for x, c in enumerate(line):
        if c != ".":
            TRUTH_COORDS.add((x, y))


def test_map_parsing() -> None:
    parsed_coords = parse_galaxy_map(SAMPLE_INPUT)
    assert parsed_coords == TRUTH_COORDS


GALAXY_DIST_TEST_CASES = (
    ((1, 6), (5, 11), 9),
    ((4, 0), (9, 10), 15),
    ((0, 2), (12, 7), 17),
    ((0, 11), (5, 11), 5),
)


@pytest.mark.parametrize(("origin", "destination", "truth_dist"), GALAXY_DIST_TEST_CASES)
def test_galaxy_distance(origin: COORD, destination: COORD, truth_dist: int) -> None:
    assert galaxy_dist(origin, destination) == truth_dist


SPACE_SCALING_TEST_CASES = (
    (2, 374),
    (10, 1030),
    (100, 8410),
)


@pytest.mark.parametrize(("scale_factor", "truth_pdist_sum"), SPACE_SCALING_TEST_CASES)
def test_space_scaling_pdist_sum(scale_factor: int, truth_pdist_sum: int) -> None:
    parsed_coords = parse_galaxy_map(SAMPLE_INPUT, scale_factor=scale_factor)
    assert sum_galaxy_pdist(parsed_coords) == truth_pdist_sum
