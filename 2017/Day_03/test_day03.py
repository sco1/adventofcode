import pytest

from .AoC2017_Day3 import stress_test, walk_spiral

PART_ONE_CASES = (
    (1, 0),
    (12, 3),
    (23, 2),
    (1024, 31),
)


@pytest.mark.parametrize(("target_square", "truth_steps"), PART_ONE_CASES)
def test_part_one(target_square: int, truth_steps: int) -> None:
    assert walk_spiral(target_square) == truth_steps


PART_TWO_CASES = (
    (3, 4),
    (24, 25),
    (25, 26),
    (55, 57),
)


@pytest.mark.parametrize(("target_value", "truth_value"), PART_TWO_CASES)
def test_part_two(target_value: int, truth_value: int) -> None:
    assert stress_test(target_value) == truth_value
