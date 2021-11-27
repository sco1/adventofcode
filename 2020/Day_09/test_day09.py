from textwrap import dedent

from .aoc_2020_day09 import find_weakness, process_stream

SAMPLE_STREAM = dedent(
    """\
    35
    20
    15
    25
    47
    40
    62
    55
    65
    95
    102
    117
    150
    182
    127
    219
    299
    277
    309
    576
    """
)

INT_STREAM = [int(line) for line in SAMPLE_STREAM.splitlines()]


def test_part_one() -> None:
    """Check that the correct stream weakness is identified for Part One."""
    assert process_stream(INT_STREAM, preamble_len=5) == 127


def test_part_two() -> None:
    """Check that the correct segment sum is calculated for the weakness window in Part Two."""
    assert find_weakness(INT_STREAM, preamble_len=5) == 62
