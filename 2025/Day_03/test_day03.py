import pytest

from .aoc_2025_day03 import find_max_joltage

JOLTAGE_TEST_CASES = (
    ("987654321111111", 2, 98),
    ("811111111111119", 2, 89),
    ("234234234234278", 2, 78),
    ("818181911112111", 2, 92),
    ("987654321111111", 12, 987_654_321_111),
    ("811111111111119", 12, 811_111_111_119),
    ("234234234234278", 12, 434_234_234_278),
    ("818181911112111", 12, 888_911_112_111),
)


@pytest.mark.parametrize(("battery_bank", "select_n", "truth_out"), JOLTAGE_TEST_CASES)
def test_max_joltage(battery_bank: str, select_n: int, truth_out: int) -> None:
    assert find_max_joltage(battery_bank, select_n) == truth_out
