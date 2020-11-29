import typing as t
from textwrap import dedent

import pytest
from aoc_2015_day8 import size_if_escaped, size_in_code, size_in_memory


class PuzzleTestCase(t.NamedTuple):
    """Helper test case representation."""

    sample_string: str
    n_string_char: int  # Size in code
    n_char: int  # Size in memory
    escaped_len: int


puzzle_input = dedent(
    r"""
    ""
    "abc"
    "aaa\"aaa"
    "\x27"
    """
)[1:].splitlines()
test_cases = [
    PuzzleTestCase(puzzle_input[0], 2, 0, 6),
    PuzzleTestCase(puzzle_input[1], 5, 3, 9),
    PuzzleTestCase(puzzle_input[2], 10, 7, 16),
    PuzzleTestCase(puzzle_input[3], 6, 1, 11),
]


@pytest.mark.parametrize("sample_str,n_string_char,n_char,escaped_len", test_cases)
def test_length_calcs(sample_str: str, n_string_char: int, n_char: int, escaped_len: int) -> None:
    """Check length calculation functions against the provided sample strings."""
    assert size_in_code(sample_str) == n_string_char
    assert size_in_memory(sample_str) == n_char
    assert size_if_escaped(sample_str) == escaped_len
