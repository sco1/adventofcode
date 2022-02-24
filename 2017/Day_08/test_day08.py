from textwrap import dedent

from .AoC2017_Day8 import execute

SAMPLE_INSTRUCTIONS = dedent(
    """\
    b inc 5 if a > 1
    a inc 1 if b < 5
    c dec -10 if a >= 1
    c inc -20 if c == 10
    """
).splitlines()


def test_part_one() -> None:
    max_val, _ = execute(SAMPLE_INSTRUCTIONS)
    assert max_val == 1


def test_part_two() -> None:
    _, programmatic_max = execute(SAMPLE_INSTRUCTIONS)
    assert programmatic_max == 10
