import pytest

from .AoC2017_Day1 import solve_captcha

PART_ONE_CASES = (
    ("1122", 3),
    ("1111", 4),
    ("1234", 0),
    ("91212129", 9),
)


@pytest.mark.parametrize(("captcha", "truth_solution"), PART_ONE_CASES)
def test_part_one(captcha: str, truth_solution: int) -> None:
    assert solve_captcha(captcha) == truth_solution


PART_TWO_CASES = (
    ("1212", 6),
    ("1221", 0),
    ("123425", 4),
    ("123123", 12),
    ("12131415", 4),
)


@pytest.mark.parametrize(("captcha", "truth_solution"), PART_TWO_CASES)
def test_part_two(captcha: str, truth_solution: int) -> None:
    assert solve_captcha(captcha, use_half_jump=True) == truth_solution
