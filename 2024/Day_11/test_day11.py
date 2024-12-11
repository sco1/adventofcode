import pytest

from .aoc_2024_day11 import blink, blink_n_counts, parse_stones


def test_parse_stones() -> None:
    assert parse_stones("0 1 10 99 999") == [0, 1, 10, 99, 999]


# fmt: off
BRUTE_BLINK_TEST_CASES = (
    ([0, 1, 10, 99, 999], 1, [1, 2024, 1, 0, 9, 9, 2_021_976]),
    ([125, 17], 1, [253_000, 1, 7]),
    ([125, 17], 2, [253, 0, 2024, 14_168]),
    ([125, 17], 3, [512_072, 1, 20, 24, 28_676_032]),
    ([125, 17], 4, [512, 72, 2024, 2, 0, 2, 4, 2867, 6032]),
    ([125, 17], 5, [1_036_288, 7, 2, 20, 24, 4048, 1, 4048, 8096, 28, 67, 60, 32]),
    ([125, 17], 6, [2_097_446_912, 14168, 4048, 2, 0, 2, 4, 40, 48, 2024, 40, 48, 80, 96, 2, 8, 6, 7, 6, 0, 3, 2]),
)
# fmt: on


@pytest.mark.parametrize(("start_stones", "n_blinks", "truth_stones"), BRUTE_BLINK_TEST_CASES)
def test_brute_blinks(start_stones: list[int], n_blinks: int, truth_stones: list[int]) -> None:
    stones = start_stones
    for _ in range(n_blinks):
        stones = blink(stones)

    assert stones == truth_stones


def test_n_stones_brute() -> None:
    stones = parse_stones("125 17")
    for _ in range(25):
        stones = blink(stones)

    assert len(stones) == 55_312


BLINK_COUNT_TEST_CASES = (
    ([0, 1, 10, 99, 999], 1, 7),
    ([125, 17], 1, 3),
    ([125, 17], 2, 4),
    ([125, 17], 3, 5),
    ([125, 17], 4, 9),
    ([125, 17], 5, 13),
    ([125, 17], 6, 22),
    ([125, 17], 25, 55_312),
)


@pytest.mark.parametrize(("start_stones", "n_blinks", "truth_count"), BLINK_COUNT_TEST_CASES)
def test_blink_count(start_stones: list[int], n_blinks: int, truth_count: int) -> None:
    assert blink_n_counts(start_stones, n_blinks) == truth_count
