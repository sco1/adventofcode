import pytest

from .aoc_2018_day1 import part1, part2

PART_ONE_TEST_CASES = (
    ("+1\n-2\n+3\n+1", 3),
    ("+1\n+1\n+1", 3),
    ("+1\n+1\n-2", 0),
    ("-1\n-2\n-3", -6),
)


@pytest.mark.parametrize(("frequency_changes, truth_frequency"), PART_ONE_TEST_CASES)
def test_part_one(frequency_changes: str, truth_frequency: int) -> None:
    changes = [int(freq) for freq in frequency_changes.splitlines()]
    assert part1(changes) == truth_frequency


PART_TWO_TEST_CASES = (
    ("+1\n-1", 0),
    ("+3\n+3\n+4\n-2\n-4", 10),
    ("-6\n+3\n+8\n+5\n-6", 5),
    ("+7\n+7\n-2\n-7\n-4", 14),
)


@pytest.mark.parametrize(("frequency_changes, truth_first_repeat"), PART_TWO_TEST_CASES)
def test_part_two(frequency_changes: str, truth_first_repeat: int) -> None:
    changes = [int(freq) for freq in frequency_changes.splitlines()]
    assert part2(changes) == truth_first_repeat
