from textwrap import dedent

import pytest

from .aoc_2023_day21 import build_garden_network, parse_garden_map, step_search

SAMPLE_INPUT = dedent(
    """\
    ...........
    .....###.#.
    .###.##..#.
    ..#.#...#..
    ....#.#....
    .##..S####.
    .##..#...#.
    .......##..
    .##.#.####.
    .##..##.##.
    ...........
    """
)


def test_map_parsing() -> None:
    plots, rocks, start = parse_garden_map(SAMPLE_INPUT)
    assert len(plots) == 81
    assert len(rocks) == 40
    assert start in plots


def test_n_reached() -> None:
    plots, rocks, start = parse_garden_map(SAMPLE_INPUT)
    n = build_garden_network(plots, rocks)
    assert len(step_search(n, start, 6)) == 16


INFINITE_GRID_CASES = (
    (6, 16),
    (10, 50),
    (50, 1594),
    (100, 6536),
    (500, 167_004),
    (1000, 668_697),
    (5000, 16_733_044),
)


@pytest.mark.skip(reason="Not implemented")
@pytest.mark.parametrize(("n_steps", "truth_reachable"), INFINITE_GRID_CASES)
def test_infinite_grid(n_steps: int, truth_reachable: int) -> None:
    ...
