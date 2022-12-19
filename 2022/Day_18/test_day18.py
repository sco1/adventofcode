from textwrap import dedent

import pytest

from .aoc_2022_day18 import calc_exterior_surface_area, calc_surface_area, parse_lava_scan

SAMPLE_GRIDS = (
    (
        dedent(
            """\
            1,1,1
            2,1,1
            """
        ),
        10,
    ),
    (
        dedent(
            """\
            2,2,2
            1,2,2
            3,2,2
            2,1,2
            2,3,2
            2,2,1
            2,2,3
            2,2,4
            2,2,6
            1,2,5
            3,2,5
            2,1,5
            2,3,5
            """
        ),
        64,
    ),
)


@pytest.mark.parametrize(("lava_scan", "truth_sides"), SAMPLE_GRIDS)
def test_part_one(lava_scan: str, truth_sides: int) -> None:
    cubes = parse_lava_scan(lava_scan)
    assert calc_surface_area(cubes) == truth_sides


SAMPLE_INPUT = dedent(
    """\
    2,2,2
    1,2,2
    3,2,2
    2,1,2
    2,3,2
    2,2,1
    2,2,3
    2,2,4
    2,2,6
    1,2,5
    3,2,5
    2,1,5
    2,3,5
    """
)


def test_part_two() -> None:
    cubes = parse_lava_scan(SAMPLE_INPUT)
    assert calc_exterior_surface_area(cubes) == 58
