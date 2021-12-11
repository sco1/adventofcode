from textwrap import dedent

import numpy as np

from .aoc_2021_day09 import (
    find_low_points,
    n_largest_basins,
    parse_topography,
    total_risk_level,
)

SAMPLE_INPUT = dedent(
    """\
    2199943210
    3987894921
    9856789892
    8767896789
    9899965678
    """
).splitlines()
TOPO_MAP = parse_topography(SAMPLE_INPUT)


def test_part_one() -> None:
    low_points = find_low_points(TOPO_MAP)
    assert total_risk_level(low_points) == 15


def test_part_two() -> None:
    three_largest = n_largest_basins(TOPO_MAP, 3)
    assert np.prod(three_largest) == 1134
