import pytest

from .aoc_2025_day05 import collapse_ranges, is_fresh, n_fresh, parse_database

SAMPLE_INPUT = """\
3-5
10-14
16-20
12-18

1
5
8
11
17
32
"""

TRUTH_RANGES = [
    (3, 5),
    (10, 14),
    (12, 18),
    (16, 20),
]

TRUTH_INGREDIENTS = [1, 5, 8, 11, 17, 32]


def test_parse_database() -> None:
    fresh_ranges, ingredients = parse_database(SAMPLE_INPUT)
    assert fresh_ranges == TRUTH_RANGES
    assert ingredients == TRUTH_INGREDIENTS


FRESH_TEST_CASES = (
    (1, False),
    (5, True),
    (8, False),
    (11, True),
    (17, True),
    (32, False),
)


@pytest.mark.parametrize(("ingredient_id", "truth_out"), FRESH_TEST_CASES)
def test_is_fresh(ingredient_id: int, truth_out: bool) -> None:
    assert is_fresh(TRUTH_RANGES, ingredient_id) == truth_out


def test_n_fresh() -> None:
    assert n_fresh(TRUTH_RANGES, TRUTH_INGREDIENTS) == 3


def test_collapse_ranges() -> None:
    assert collapse_ranges(TRUTH_RANGES) == 14
