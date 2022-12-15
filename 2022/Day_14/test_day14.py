from textwrap import dedent

from .aoc_2022_day14 import fill_until_blocked, parse_rock_traces, simulate_sand_fill

SAMPLE_INPUT = dedent(
    """\
    498,4 -> 498,6 -> 496,6
    503,4 -> 502,4 -> 502,9 -> 494,9
    """
)


def test_part_one() -> None:
    rocks, lowest = parse_rock_traces(SAMPLE_INPUT)
    assert simulate_sand_fill(rocks, lowest) == 24


def test_part_two() -> None:
    rocks, lowest = parse_rock_traces(SAMPLE_INPUT)
    assert fill_until_blocked(rocks, lowest) == 93
