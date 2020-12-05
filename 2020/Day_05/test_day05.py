import typing as t

import pytest

from .aoc_2020_day05 import decode_boarding_pass


class DecoderTestCase(t.NamedTuple):
    """Helper container for the boarding pass decoding test cases."""

    specificer: str  # 10 letters
    row: int  # [0, 127]
    column: int  # [0, 7]
    seat_id: int  # row*8 + column


BOARDING_PASS_TEST_CASES = [
    DecoderTestCase("FBFBBFFRLR", 44, 5, 357),
    DecoderTestCase("BFFFBBFRRR", 70, 7, 567),
    DecoderTestCase("FFFBBBFRRR", 14, 7, 119),
    DecoderTestCase("BBFFBBFRLL", 102, 4, 820),
]


@pytest.mark.parametrize(("specifier", "row", "column", "seat_id"), BOARDING_PASS_TEST_CASES)
def test_boarding_pass_decoding(specifier: str, row: int, column: int, seat_id: int) -> None:
    """Check that the decoded boarding pass matches the provided truth values."""
    assert decode_boarding_pass(specifier) == (row, column, seat_id)
