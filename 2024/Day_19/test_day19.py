from textwrap import dedent

import pytest

from .aoc_2024_day19 import count_possible, is_possible, n_possible, parse_onsen_station

TOWELS = ("r", "wr", "b", "g", "bwu", "rb", "gb", "br")

DESIGN_TEST_CASES = (
    ("brwrr", True),
    ("bggr", True),
    ("gbbr", True),
    ("rrbgbr", True),
    ("ubwu", False),
    ("bwurrg", True),
    ("brgr", True),
    ("bbrgwb", False),
)


@pytest.mark.parametrize(("pattern", "truth_is_possible"), DESIGN_TEST_CASES)
def test_is_possible(pattern: str, truth_is_possible: bool) -> None:
    assert is_possible(TOWELS, pattern) == truth_is_possible


SAMPLE_INPUT = dedent(
    """\
    r, wr, b, g, bwu, rb, gb, br

    brwrr
    bggr
    gbbr
    rrbgbr
    ubwu
    bwurrg
    brgr
    bbrgwb
    """
)


def test_n_possible() -> None:
    towels, patterns = parse_onsen_station(SAMPLE_INPUT)
    assert count_possible(towels, patterns) == 6


COUNT_TEST_CASES = (
    ("brwrr", 2),
    ("bggr", 1),
    ("gbbr", 4),
    ("rrbgbr", 6),
    ("ubwu", 0),
    ("bwurrg", 1),
    ("brgr", 2),
    ("bbrgwb", 0),
)


@pytest.mark.parametrize(("pattern", "truth_count"), COUNT_TEST_CASES)
def test_n_arrangements(pattern: str, truth_count: bool) -> None:
    assert n_possible(TOWELS, pattern) == truth_count
