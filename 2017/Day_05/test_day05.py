from textwrap import dedent

from .AoC2017_Day5 import follow_jumps, follow_strange_jumps

SAMPLE_OFFSETS = dedent(
    """\
    0
    3
    0
    1
    -3
    """
)


def test_part_one() -> None:
    jumps = [int(jump) for jump in SAMPLE_OFFSETS.split()]
    assert follow_jumps(jumps) == 5


def test_part_two() -> None:
    jumps = [int(jump) for jump in SAMPLE_OFFSETS.split()]
    assert follow_strange_jumps(jumps) == 10
