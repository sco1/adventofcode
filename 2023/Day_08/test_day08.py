from textwrap import dedent

import pytest

from .aoc_2023_day08 import parse_map, traverse_as_ghost, traverse_as_ghost_bf, traverse_map

SAMPLE_MAP_1 = dedent(
    """\
    RL

    AAA = (BBB, CCC)
    BBB = (DDD, EEE)
    CCC = (ZZZ, GGG)
    DDD = (DDD, DDD)
    EEE = (EEE, EEE)
    GGG = (GGG, GGG)
    ZZZ = (ZZZ, ZZZ)
    """
)

SAMPLE_MAP_2 = dedent(
    """\
    LLR

    AAA = (BBB, BBB)
    BBB = (AAA, ZZZ)
    ZZZ = (ZZZ, ZZZ)
    """
)


def test_map_parse() -> None:
    instructions, nodes = parse_map(SAMPLE_MAP_2)
    assert instructions == "LLR"
    assert nodes == {"AAA": ("BBB", "BBB"), "BBB": ("AAA", "ZZZ"), "ZZZ": ("ZZZ", "ZZZ")}


MAP_TRAVERSAL_TEST_CASES = (
    (SAMPLE_MAP_1, 2),
    (SAMPLE_MAP_2, 6),
)


@pytest.mark.parametrize(("raw_map", "truth_n_steps"), MAP_TRAVERSAL_TEST_CASES)
def test_map_traversal(raw_map: str, truth_n_steps: int) -> None:
    instructions, nodes = parse_map(raw_map)
    assert traverse_map(instructions, nodes) == truth_n_steps


SAMPLE_MAP_GHOSTS = dedent(
    """\
    LR

    11A = (11B, XXX)
    11B = (XXX, 11Z)
    11Z = (11B, XXX)
    22A = (22B, XXX)
    22B = (22C, 22C)
    22C = (22Z, 22Z)
    22Z = (22B, 22B)
    XXX = (XXX, XXX)
    """
)


def test_ghost_traversal() -> None:
    instructions, nodes = parse_map(SAMPLE_MAP_GHOSTS)
    assert traverse_as_ghost_bf(instructions, nodes) == 6
    assert traverse_as_ghost(instructions, nodes) == 6
