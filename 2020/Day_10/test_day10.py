import typing as t
from textwrap import dedent

import pytest

from .aoc_2020_day10 import build_graph, find_adapter_chain, n_paths


class AdapterTestCase(t.NamedTuple):  # noqa: D101
    joltage_ratings: str
    n_one_jolt: int
    n_three_jolt: int
    n_arrangements: int


PUZZLE_TEST_CASES = [
    AdapterTestCase(
        dedent(
            """\
            16
            10
            15
            5
            1
            11
            7
            19
            6
            12
            4
            """
        ),
        7,
        5,
        8,
    ),
    AdapterTestCase(
        dedent(
            """\
            28
            33
            18
            42
            31
            14
            46
            20
            48
            47
            24
            23
            49
            45
            19
            38
            39
            11
            1
            32
            25
            35
            8
            17
            7
            9
            4
            2
            34
            10
            3
            """
        ),
        22,
        10,
        19208,
    ),
]


@pytest.mark.parametrize(
    ("joltage_ratings", "n_one_jolt", "n_three_jolt", "n_arrangements"), PUZZLE_TEST_CASES
)
def test_joltage_chain(
    joltage_ratings: str, n_one_jolt: int, n_three_jolt: int, n_arrangements: int
) -> None:
    """Check for correct algorithms for parts 1 & 2."""
    adapter_graph = build_graph(joltage_ratings)
    assert find_adapter_chain(adapter_graph) == (n_one_jolt, n_three_jolt)
    assert n_paths(adapter_graph) == n_arrangements
