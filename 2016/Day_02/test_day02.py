from textwrap import dedent

import pytest

from .aoc_2016_day02 import DIAMOND_KEYPAD, KEYPAD, find_bathroom_code, parse_keypad

SAMPLE_INPUT = dedent(
    """\
    ULL
    RRDDD
    LURDL
    UUUUD
    """
)


TEST_CASES = (
    (KEYPAD, "1985"),
    (DIAMOND_KEYPAD, "5DB3"),
)


@pytest.mark.parametrize(("raw_keypad", "truth_code"), TEST_CASES)
def test_bathroom_code(raw_keypad: str, truth_code: str) -> None:
    keypad, start_loc = parse_keypad(raw_keypad)
    assert find_bathroom_code(SAMPLE_INPUT, keypad, start_loc) == truth_code
