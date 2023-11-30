import pytest

from .aoc_2022_day01 import first_repeat_block_distance, headquarters_distance

SAMPLE_CASES = (
    ("R2, L3", 5),
    ("R2, R2, R2", 2),
    ("R5, L5, R5, R3", 12),
)


@pytest.mark.parametrize(("instructions", "truth_distance"), SAMPLE_CASES)
def test_instruction_distance(instructions: str, truth_distance: int) -> None:
    assert headquarters_distance(instructions) == truth_distance


def test_first_repeat_distance() -> None:
    instructions = "R8, R4, R4, R8"
    assert first_repeat_block_distance(instructions) == 4
