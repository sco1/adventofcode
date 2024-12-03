import pytest

from .aoc_2024_day03 import calculate_instruction_result, find_operands

SAMPLE_INPUT = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"

INSTRUCTION_TEST_CASES = (
    ("mul(4*", None),
    ("mul(6,9!", None),
    ("?(12,34)", None),
    ("mul ( 2 , 4 )", None),
    ("mul(44,46)", [[44, 46]]),
    ("mul(123,4)", [[123, 4]]),
    (SAMPLE_INPUT, [[2, 4], [5, 5], [11, 8], [8, 5]]),
)


@pytest.mark.parametrize(("instruction", "truth_operands"), INSTRUCTION_TEST_CASES)
def test_find_operands(instruction: str, truth_operands: list[list[int]] | None) -> None:
    assert find_operands(instruction) == truth_operands


CALCULATION_TEST_CASES = (
    ("mul(4*", 0),
    ("mul(6,9!", 0),
    ("?(12,34)", 0),
    ("mul ( 2 , 4 )", 0),
    ("mul(44,46)", 2024),
    ("mul(123,4)", 492),
    (SAMPLE_INPUT, 161),
)


@pytest.mark.parametrize(("instruction", "truth_result"), CALCULATION_TEST_CASES)
def test_calculate_result(instruction: str, truth_result: int) -> None:
    assert calculate_instruction_result(instruction) == truth_result


def test_do_dont_calculation() -> None:
    instruction = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    assert calculate_instruction_result(instruction, do_dont=True) == 48
