from textwrap import dedent

import networkx as nx
import pytest

from .aoc_2024_day12 import build_plant_graph, calculate_fence_cost, calculate_bulk_fence_cost

SAMPLE_INPUT_1 = dedent(
    """\
    AAAA
    BBCD
    BBCC
    EEEC
    """
)

SAMPLE_INPUT_2 = dedent(
    """\
    OOOOO
    OXOXO
    OOOOO
    OXOXO
    OOOOO
    """
)

SAMPLE_INPUT_3 = dedent(
    """\
    RRRRIICCFF
    RRRRIICCCF
    VVRRRCCFFF
    VVRCCCJFFF
    VVVVCJJCFE
    VVIVCCJJEE
    VVIIICJJEE
    MIIIIIJJEE
    MIIISIJEEE
    MMMISSJEEE
    """
)

REGION_TEST_CASES = (
    (SAMPLE_INPUT_1, 5),
    (SAMPLE_INPUT_2, 5),
    (SAMPLE_INPUT_3, 11),
)


@pytest.mark.parametrize(("plant_map", "truth_n_regions"), REGION_TEST_CASES)
def test_map_parsing(plant_map: str, truth_n_regions: int) -> None:
    pg = build_plant_graph(plant_map)

    regions = list(nx.connected_components(pg))
    assert len(regions) == truth_n_regions


FENCE_COST_TEST_CASES = (
    (SAMPLE_INPUT_1, 140),
    (SAMPLE_INPUT_2, 772),
    (SAMPLE_INPUT_3, 1930),
)


@pytest.mark.parametrize(("plant_map", "truth_fence_cost"), FENCE_COST_TEST_CASES)
def test_calculate_fence_cost(plant_map: str, truth_fence_cost: int) -> None:
    pg = build_plant_graph(plant_map)
    assert calculate_fence_cost(pg) == truth_fence_cost


SAMPLE_INPUT_4 = dedent(
    """\
    EEEEE
    EXXXX
    EEEEE
    EXXXX
    EEEEE
    """
)

SAMPLE_INPUT_5 = dedent(
    """\
    AAAAAA
    AAABBA
    AAABBA
    ABBAAA
    ABBAAA
    AAAAAA
    """
)

FENCE_BULK_COST_TEST_CASES = (
    (SAMPLE_INPUT_1, 80),
    (SAMPLE_INPUT_3, 1206),
    (SAMPLE_INPUT_4, 236),
    (SAMPLE_INPUT_5, 368),
)


@pytest.mark.parametrize(("plant_map", "truth_fence_cost"), FENCE_COST_TEST_CASES)
def test_calculate_bulk_fence_cost(plant_map: str, truth_fence_cost: int) -> None:
    pg = build_plant_graph(plant_map)
    assert calculate_bulk_fence_cost(pg) == truth_fence_cost
