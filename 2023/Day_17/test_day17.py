from textwrap import dedent

import pytest

from helpers.geometry import COORD
from .aoc_2023_day17 import minimize_heat_loss, parse_heat_map

SAMPLE_INPUT = dedent(
    """\
    2413432311323
    3215453535623
    3255245654254
    3446585845452
    4546657867536
    1438598798454
    4457876987766
    3637877979653
    4654967986887
    4564679986453
    1224686865563
    2546548887735
    4322674655533
    """
)
HEAT_MAP = parse_heat_map(SAMPLE_INPUT)


def test_minimized_path() -> None:
    assert minimize_heat_loss(HEAT_MAP) == 102


ULTRA_SAMPLE_1 = dedent(
    """\
    2413432311323
    3215453535623
    3255245654254
    3446585845452
    4546657867536
    1438598798454
    4457876987766
    3637877979653
    4654967986887
    4564679986453
    1224686865563
    2546548887735
    4322674655533
    """
)

ULTRA_SAMPLE_2 = dedent(
    """\
    111111111111
    999999999991
    999999999991
    999999999991
    999999999991
    """
)

ULTRA_CRUCIBLE_CASES = (
    (parse_heat_map(ULTRA_SAMPLE_1), 94),
    (parse_heat_map(ULTRA_SAMPLE_2), 71),
)


@pytest.mark.parametrize(("heat_map", "truth_min_path"), ULTRA_CRUCIBLE_CASES)
def test_ultra_crucible(heat_map: dict[COORD, int], truth_min_path: int) -> None:
    assert minimize_heat_loss(heat_map, min_n_straight=4, max_n_straight=10) == truth_min_path
