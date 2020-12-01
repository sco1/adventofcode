from textwrap import dedent

from .aoc_2020_day01 import find_sum_combo


SAMPLE_INPUT = dedent(
    """\
    1721
    979
    366
    299
    675
    1456
    """
).splitlines()

PUZZLE_INPUT = [int(line) for line in SAMPLE_INPUT]


def test_part_one() -> None:
    """Check that the correct product of 2 entries is generated."""
    expense_product, _ = find_sum_combo(PUZZLE_INPUT)

    assert expense_product == 514579


def test_part_two() -> None:
    """Check that the correct product of 3 entries is generated."""
    expense_product, _ = find_sum_combo(PUZZLE_INPUT, n_entries=3)

    assert expense_product == 241861950
