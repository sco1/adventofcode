from textwrap import dedent

from .aoc_2021_day15 import find_route, parse_risk_map

SAMPLE_INPUT = dedent(
    """\
    1163751742
    1381373672
    2136511328
    3694931569
    7463417111
    1319128137
    1359912421
    3125421639
    1293138521
    2311944581
    """
).splitlines()


def test_part_one() -> None:
    assert find_route(*parse_risk_map(SAMPLE_INPUT)) == 40


def test_part_two() -> None:
    assert find_route(*parse_risk_map(SAMPLE_INPUT, True)) == 315
