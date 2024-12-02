from textwrap import dedent

import pytest

from .aoc_2024_day02 import is_level_safe, is_level_safe_with_dampener, parse_level_report

SAMPLE_INPUT = dedent(
    """\
    7 6 4 2 1
    1 2 7 8 9
    9 7 6 2 1
    1 3 2 4 5
    8 6 4 4 1
    1 3 6 7 9
    """
).strip()


def test_report_parse() -> None:
    truth_parsed = [
        [7, 6, 4, 2, 1],
        [1, 2, 7, 8, 9],
        [9, 7, 6, 2, 1],
        [1, 3, 2, 4, 5],
        [8, 6, 4, 4, 1],
        [1, 3, 6, 7, 9],
    ]

    assert parse_level_report(SAMPLE_INPUT) == truth_parsed


REPORT_TEST_CASES = (
    ((7, 6, 4, 2, 1), True),
    ((1, 2, 7, 8, 9), False),
    ((9, 7, 6, 2, 1), False),
    ((1, 3, 2, 4, 5), False),
    ((8, 6, 4, 4, 1), False),
    ((1, 3, 6, 7, 9), True),
    ((7, 6, 5, 6, 7), False),  # Edge case, slope changes sign
)


@pytest.mark.parametrize(("report", "truth_is_safe"), REPORT_TEST_CASES)
def test_report_safety(report: tuple[int, ...], truth_is_safe: bool) -> None:
    assert is_level_safe(report) == truth_is_safe


DAMPENER_TEST_CASES = (
    ([7, 6, 4, 2, 1], True),
    ([1, 2, 7, 8, 9], False),
    ([9, 7, 6, 2, 1], False),
    ([1, 3, 2, 4, 5], True),
    ([8, 6, 4, 4, 1], True),
    ([1, 3, 6, 7, 9], True),
    ([7, 6, 5, 6, 7], False),  # Edge case, slope changes sign
    ([1, 6, 7, 8, 9], True),  # Edge case, first level should be dropped
)


@pytest.mark.parametrize(("report", "truth_is_safe"), DAMPENER_TEST_CASES)
def test_report_safety_with_dampener(report: list[int], truth_is_safe: bool) -> None:
    assert is_level_safe_with_dampener(report) == truth_is_safe
