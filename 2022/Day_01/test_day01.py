from textwrap import dedent

from .aoc_2022_day01 import find_best_snack_trio, find_most_caloric_dense_elf, parse_puzzle_input

SAMPLE_INPUT = dedent(
    """\
    1000
    2000
    3000

    4000

    5000
    6000

    7000
    8000
    9000

    10000
    """
)
TRUTH_CALORIE_COUNT = [6_000, 4_000, 11_000, 24_000, 10_000]


def test_puzzle_conversion() -> None:
    assert parse_puzzle_input(SAMPLE_INPUT) == TRUTH_CALORIE_COUNT


def test_part_one() -> None:
    assert find_most_caloric_dense_elf(TRUTH_CALORIE_COUNT) == 24_000


def test_part_two() -> None:
    assert find_best_snack_trio(TRUTH_CALORIE_COUNT) == 45_000
