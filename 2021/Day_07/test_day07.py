from textwrap import dedent

from .aoc_2021_day07 import min_horizontal_burn

SAMPLE_INPUT = dedent(
    """\
    16,1,2,0,4,2,7,1,2,14
    """
).strip()
DISTANCES = [int(distance) for distance in SAMPLE_INPUT.split(",")]


def test_part_one() -> None:
    assert min_horizontal_burn(DISTANCES) == 37


def test_part_two() -> None:
    assert min_horizontal_burn(DISTANCES, constant_burn=False) == 168
