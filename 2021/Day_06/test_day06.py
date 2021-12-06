from textwrap import dedent

from .aoc_2021_day06 import spawn_until

SAMPLE_INPUT = dedent(
    """\
    3,4,3,1,2
    """
).strip()
AGES = [int(age) for age in SAMPLE_INPUT.split(",")]


def test_part_one() -> None:
    assert spawn_until(AGES, 80) == 5934


def test_part_two() -> None:
    assert spawn_until(AGES, 256) == 26_984_457_539
