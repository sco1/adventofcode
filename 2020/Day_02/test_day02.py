import typing as t
from textwrap import dedent

import pytest

from .aoc_2020_day02 import n_valid_passwords, parse_passwords


class PasswordTestCase(t.NamedTuple):
    """Helper container for password test cases."""

    puzzle_input: str
    n_valid_a: int  # Part 1 spec interpretation
    n_valid_b: int  # Part 2 spec interpretation


PASSWORD_TEST_CASES = [
    PasswordTestCase(
        dedent(
            """\
            1-3 a: abcde
            1-3 b: cdefg
            2-9 c: ccccccccc
            """
        ),
        2,
        1,
    ),
]


@pytest.mark.parametrize("puzzle_input,n_valid_a,n_valid_b", PASSWORD_TEST_CASES)
def test_spec_interpretation(puzzle_input: str, n_valid_a: int, n_valid_b: int) -> None:
    """Check the provided passwords & specifications against the two policy interpretations."""
    parsed_input = parse_passwords(puzzle_input.splitlines())

    assert n_valid_passwords(parsed_input) == n_valid_a
    assert n_valid_passwords(parsed_input, spec_type=1) == n_valid_b
