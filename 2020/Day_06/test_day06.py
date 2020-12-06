import typing as t
from textwrap import dedent

import pytest

from .aoc_2020_day06 import count_all_yes, count_any_yes


class CustomsTestCase(t.NamedTuple):
    """Helper container for customs form test cases."""

    raw_group_answer: str
    n_any_yes: int
    n_all_yes: int


FORM_TEST_CASES = [
    CustomsTestCase(
        dedent(
            """\
            abcx
            abcy
            abcz
            """
        ),
        6,
        3,
    ),
    CustomsTestCase(
        dedent(
            """\
            abc
            """
        ),
        3,
        3,
    ),
    CustomsTestCase(
        dedent(
            """\
            a
            b
            c
            """
        ),
        3,
        0,
    ),
    CustomsTestCase(
        dedent(
            """\
            ab
            ac
            """
        ),
        3,
        1,
    ),
    CustomsTestCase(
        dedent(
            """\
            a
            a
            a
            a
            """
        ),
        1,
        1,
    ),
    CustomsTestCase(
        dedent(
            """\
            b
            """
        ),
        1,
        1,
    ),
]


@pytest.mark.parametrize(("raw_group_answer", "n_any_yes", "n_all_yes"), FORM_TEST_CASES)
def test_group_form_parsing(raw_group_answer: str, n_any_yes: int, n_all_yes: int) -> None:
    """Check the 'yes' answer parsing for the two puzzle specifications."""
    assert count_any_yes(raw_group_answer.replace("\n", "")) == n_any_yes
    assert count_all_yes(raw_group_answer.splitlines()) == n_all_yes
