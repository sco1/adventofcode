from textwrap import dedent

import pytest

from .aoc_2021_day08 import Signal, determine_output, n_simple_outputs

SAMPLE_INPUT = dedent(
    """\
    acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf
    be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
    edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
    fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
    fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
    aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
    fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
    dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
    bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
    egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
    gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
    """
).splitlines()
PARSED_SIGNALS = Signal.from_raw(SAMPLE_INPUT)


def test_part_one() -> None:
    assert n_simple_outputs(PARSED_SIGNALS) == 26


SAMPLE_OUTPUTS = [
    5353,
    8394,
    9781,
    1197,
    9361,
    4873,
    8418,
    4548,
    1625,
    8717,
    4315,
]


@pytest.mark.parametrize(("signal", "truth_output"), zip(PARSED_SIGNALS, SAMPLE_OUTPUTS))
def test_part_two(signal: list[Signal], truth_output: int) -> None:
    assert determine_output(signal) == truth_output
