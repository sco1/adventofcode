from textwrap import dedent

from .aoc_2021_day14 import non_brute_deconstruct, parse_polymer_formula

SAMPLE_INPUT = dedent(
    """\
    NNCB

    CH -> B
    HH -> N
    CB -> H
    NH -> C
    HB -> C
    HC -> B
    HN -> C
    NN -> C
    BH -> H
    NC -> B
    NB -> B
    BN -> B
    BB -> N
    BC -> B
    CC -> N
    CN -> C
    """
)
TEMPLATE, RULES = parse_polymer_formula(SAMPLE_INPUT)


def test_part_one() -> None:
    assert non_brute_deconstruct(TEMPLATE, RULES, 10) == 1588


def test_part_two() -> None:
    assert non_brute_deconstruct(TEMPLATE, RULES, 40) == 2188189693529
