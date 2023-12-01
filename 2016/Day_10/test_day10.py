import math
from textwrap import dedent

from .aoc_2022_day10 import Factory

SAMPLE_INPUT = dedent(
    """\
    value 5 goes to bot 2
    bot 2 gives low to bot 1 and high to bot 0
    value 3 goes to bot 1
    bot 1 gives low to output 1 and high to bot 0
    bot 0 gives low to output 2 and high to output 0
    value 2 goes to bot 2
    """
)


def test_who_compared() -> None:
    fact = Factory(SAMPLE_INPUT)
    assert fact.who_compared((2, 5)) == 2


def test_output_prod() -> None:
    fact = Factory(SAMPLE_INPUT)
    assert math.prod((fact.outputs[idx].chips[0] for idx in (0, 1, 2))) == 30
