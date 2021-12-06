from textwrap import dedent

from .aoc_2021_day05 import find_overlaps

SAMPLE_INPUT = dedent(
    """\
    0,9 -> 5,9
    8,0 -> 0,8
    9,4 -> 3,4
    2,2 -> 2,1
    7,0 -> 7,4
    6,4 -> 2,0
    0,9 -> 2,9
    3,4 -> 1,4
    0,0 -> 8,8
    5,5 -> 8,2
    """
).splitlines()


def test_part_one() -> None:
    assert find_overlaps(SAMPLE_INPUT) == 5


def test_part_two() -> None:
    assert find_overlaps(SAMPLE_INPUT, ignore_diag=False) == 12
