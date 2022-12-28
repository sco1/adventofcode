from textwrap import dedent

import pytest

from .aoc_2022_day25 import calculate_fuel_requirement, dec2sanfu, snafu2dec

DECIMAL_TO_SNAFU = (
    (1, "1"),
    (2, "2"),
    (3, "1="),
    (4, "1-"),
    (5, "10"),
    (6, "11"),
    (7, "12"),
    (8, "2="),
    (9, "2-"),
    (10, "20"),
    (15, "1=0"),
    (20, "1-0"),
    (2022, "1=11-2"),
    (12345, "1-0---0"),
    (314159265, "1121-1110-1=0"),
)


@pytest.mark.parametrize(("decimal_val", "truth_snafu"), DECIMAL_TO_SNAFU)
def test_decimal_to_snafu(decimal_val: int, truth_snafu: str) -> None:
    assert dec2sanfu(decimal_val) == truth_snafu


SNAFU_TO_DECIMAL = (
    ("1=-0-2", 1747),
    ("12111", 906),
    ("2=0=", 198),
    ("21", 11),
    ("2=01", 201),
    ("111", 31),
    ("20012", 1257),
    ("112", 32),
    ("1=-1=", 353),
    ("1-12", 107),
    ("12", 7),
    ("1=", 3),
    ("122", 37),
)


@pytest.mark.parametrize(("snafu_val", "truth_decimal"), SNAFU_TO_DECIMAL)
def test_snafu_to_decimal(snafu_val: str, truth_decimal: int) -> None:
    assert snafu2dec(snafu_val) == truth_decimal


SAMPLE_INPUT = dedent(
    """\
    1=-0-2
    12111
    2=0=
    21
    2=01
    111
    20012
    112
    1=-1=
    1-12
    12
    1=
    122
    """
)


def test_part_one() -> None:
    assert calculate_fuel_requirement(SAMPLE_INPUT) == ("2=-1=0", 4890)
