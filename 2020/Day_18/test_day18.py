import pytest

from .aoc_2020_day18 import calc_equation

SAMPLE_EQUATIONS = [
    ("1 + 2 * 3 + 4 * 5 + 6", 71, 231),
    ("1 + (2 * 3) + (4 * (5 + 6))", 51, 51),
    ("2 * 3 + (4 * 5)", 26, 46),
    ("5 + (8 * 3 + 9 + 3 * 4 * 3)", 437, 1445),
    ("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 12240, 669060),
    ("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 13632, 23340),
]


@pytest.mark.parametrize(("equation", "check_val_p1", "check_val_p2"), SAMPLE_EQUATIONS)
def test_north_pole_math(equation: str, check_val_p1: int, check_val_p2: int) -> None:
    """Check for correct calculation of the equation using the two sets of math rules."""
    assert calc_equation(equation) == check_val_p1
    assert calc_equation(equation, is_advanced_math=True) == check_val_p2
