from textwrap import dedent

import pytest

from .AoC2017_Day2 import checksum_divisible, checksum_minmax, parse_spreadsheet

PART_ONE_CASES = (
    (
        dedent(
            """\
            5 1 9 5
            7 5 3
            2 4 6 8
            """
        ).splitlines(),
        18,
    ),
)


@pytest.mark.parametrize(("raw_spreadsheet", "truth_solution"), PART_ONE_CASES)
def test_part_one(raw_spreadsheet: list[str], truth_solution: int) -> None:
    spreadsheet = parse_spreadsheet(raw_spreadsheet)
    assert checksum_minmax(spreadsheet) == truth_solution


PART_TWO_CASES = (
    (
        dedent(
            """\
            5 9 2 8
            9 4 7 3
            3 8 6 5
            """
        ).splitlines(),
        9,
    ),
)


@pytest.mark.parametrize(("raw_spreadsheet", "truth_solution"), PART_TWO_CASES)
def test_part_two(raw_spreadsheet: list[str], truth_solution: int) -> None:
    spreadsheet = parse_spreadsheet(raw_spreadsheet)
    assert checksum_divisible(spreadsheet) == truth_solution
