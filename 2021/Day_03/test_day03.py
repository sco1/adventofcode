from textwrap import dedent

from .aoc_2021_day03 import calculate_life_support_rating, calculate_power_consumption

SAMPLE_INPUT = dedent(
    """\
    00100
    11110
    10110
    10111
    10101
    01111
    00111
    11100
    10000
    11001
    00010
    01010
    """
).splitlines()


def test_part_one() -> None:
    assert calculate_power_consumption(SAMPLE_INPUT) == 198


def test_part_two() -> None:
    assert calculate_life_support_rating(SAMPLE_INPUT) == 230
