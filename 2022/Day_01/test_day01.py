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


def test_puzzle_conversion() -> None:
    assert parse_puzzle_input(SAMPLE_INPUT) == [6_000, 4_000, 11_000, 24_000, 10_000]


def test_part_one() -> None:
    puzzle_input = parse_puzzle_input(SAMPLE_INPUT)
    assert find_most_caloric_dense_elf(puzzle_input) == 24_000


def test_part_two() -> None:
    puzzle_input = parse_puzzle_input(SAMPLE_INPUT)
    assert find_best_snack_trio(puzzle_input) == 45_000
