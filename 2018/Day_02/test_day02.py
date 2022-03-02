from textwrap import dedent

from .aoc_2018_day2 import part1, part2

PART_ONE_SAMPLE = dedent(
    """\
    abcdef
    bababc
    abbcde
    abcccd
    aabcdd
    abcdee
    ababab
    """
).splitlines()


def test_part_one() -> None:
    assert part1(PART_ONE_SAMPLE) == 12


PART_TWO_SAMPLE = dedent(
    """\
    abcde
    fghij
    klmno
    pqrst
    fguij
    axcye
    wvxyz
    """
).splitlines()


def test_part_two() -> None:
    assert part2(PART_TWO_SAMPLE) == "fgij"
