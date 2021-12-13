from textwrap import dedent

from .aoc_2021_day13 import fold_paper, parse_instructions, prettyprint

SAMPLE_INPUT = dedent(
    """\
    6,10
    0,14
    9,10
    0,3
    10,4
    4,11
    6,0
    6,12
    4,1
    0,13
    10,12
    3,4
    3,0
    8,4
    1,10
    2,14
    8,10
    9,0

    fold along y=7
    fold along x=5
    """
)
DOT_COORDS, FOLDS = parse_instructions(SAMPLE_INPUT)


def test_part_one() -> None:
    assert len(fold_paper(DOT_COORDS, [FOLDS[0]])) == 17


EXPECTED_PRETTYPRINT = dedent(
    """\
    #####
    #   #
    #   #
    #   #
    #####"""
)


def test_part_two() -> None:
    folded = fold_paper(DOT_COORDS, FOLDS)
    assert prettyprint(folded) == EXPECTED_PRETTYPRINT
