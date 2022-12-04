from textwrap import dedent

import pytest

from .aoc_2022_day04 import check_any_overlap, check_full_overlap, count_overlaps, parse_assignments

SAMPLE_ASSIGNMENTS_CHECK_FULL = (
    ("2-4,6-8", False),
    ("2-3,4-5", False),
    ("5-7,7-9", False),
    ("2-8,3-7", True),
    ("6-6,4-6", True),
    ("2-6,4-8", False),
)


@pytest.mark.parametrize(("assignments, is_fully_contained"), SAMPLE_ASSIGNMENTS_CHECK_FULL)
def test_assignment_contain(assignments: str, is_fully_contained: bool) -> None:
    parsed = parse_assignments([assignments])[0]
    assert check_full_overlap(parsed) == is_fully_contained


SAMPLE_INPUT = dedent(
    """\
    2-4,6-8
    2-3,4-5
    5-7,7-9
    2-8,3-7
    6-6,4-6
    2-6,4-8
    """
)


def test_overlap_count() -> None:
    assert count_overlaps(SAMPLE_INPUT.splitlines()) == (2, 4)


SAMPLE_ASSIGNMENTS_CHECK_ANY = (
    ("2-4,6-8", False),
    ("2-3,4-5", False),
    ("5-7,7-9", True),
    ("2-8,3-7", True),
    ("6-6,4-6", True),
    ("2-6,4-8", True),
)


@pytest.mark.parametrize(("assignments, has_any_overlap"), SAMPLE_ASSIGNMENTS_CHECK_ANY)
def test_any_overlap(assignments: str, has_any_overlap: bool) -> None:
    parsed = parse_assignments([assignments])[0]
    assert check_any_overlap(parsed) == has_any_overlap
