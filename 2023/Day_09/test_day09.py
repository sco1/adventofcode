import pytest

from .aoc_2023_day09 import extrapolate

TEST_CASES = (
    ("0 3 6 9 12 15", 18),
    ("1 3 6 10 15 21", 28),
    ("10 13 16 21 30 45", 68),
)


@pytest.mark.parametrize(("history", "truth_next_val"), TEST_CASES)
def test_extrapolation(history: str, truth_next_val: int) -> None:
    assert extrapolate(history) == truth_next_val


TEST_CASES_REWIND = (
    ("0 3 6 9 12 15", -3),
    ("1 3 6 10 15 21", 0),
    ("10 13 16 21 30 45", 5),
)


@pytest.mark.parametrize(("history", "truth_next_val"), TEST_CASES_REWIND)
def test_reverse_extrapolation(history: str, truth_next_val: int) -> None:
    assert extrapolate(history, rewind=True) == truth_next_val
