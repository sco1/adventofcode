from textwrap import dedent

import pytest

from .aoc_2024_day10 import find_all_trails, find_good_trails, parse_topo_map

SAMPLE_INPUT = dedent(
    """\
    0123
    1234
    8765
    9876
    """
)

LARGER_SAMPLE_INPUT = dedent(
    """\
    89010123
    78121874
    87430965
    96549874
    45678903
    32019012
    01329801
    10456732
    """
)

TRAILHEAD_TEST_CASES = (
    (SAMPLE_INPUT, 1),
    (LARGER_SAMPLE_INPUT, 9),
)


@pytest.mark.parametrize(("raw_map", "truth_n_trailheads"), TRAILHEAD_TEST_CASES)
def test_map_parse(raw_map: str, truth_n_trailheads: int) -> None:
    # Height parsing is simple enough that we'll just test the trailhead extraction contents
    _, trailheads = parse_topo_map(raw_map)
    assert len(trailheads) == truth_n_trailheads


GOOD_HIKE_TEST_CASES = (
    (SAMPLE_INPUT, 1),
    (LARGER_SAMPLE_INPUT, 36),
)


@pytest.mark.parametrize(("raw_map", "truth_n_good_trailheads"), GOOD_HIKE_TEST_CASES)
def test_good_trails(raw_map: str, truth_n_good_trailheads: int) -> None:
    assert find_good_trails(*parse_topo_map(raw_map)) == truth_n_good_trailheads


def test_all_trails() -> None:
    assert find_all_trails(*parse_topo_map(LARGER_SAMPLE_INPUT)) == 81
