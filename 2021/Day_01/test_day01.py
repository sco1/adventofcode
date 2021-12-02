from textwrap import dedent

from .aoc_2021_day01 import count_ascending

SAMPLE_INPUT = dedent(
    """\
    199
    200
    208
    210
    200
    207
    240
    269
    260
    263
    """
).splitlines()

PUZZLE_INPUT = [int(line) for line in SAMPLE_INPUT]


def test_part_one() -> None:
    n_ascending = count_ascending(PUZZLE_INPUT, 1)

    assert n_ascending == 7


def test_part_two() -> None:
    n_ascending = count_ascending(PUZZLE_INPUT, 3)

    assert n_ascending == 5
