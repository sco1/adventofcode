from textwrap import dedent

from .aoc_2016_day08 import Screen, calculate_lit_pixels, parse_instructions

SAMPLE_INPUT = dedent(
    """\
    rect 3x2
    rotate column x=1 by 1
    rotate row y=0 by 4
    rotate column x=1 by 1
    """
)


def test_n_lit() -> None:
    instructions = parse_instructions(SAMPLE_INPUT)
    assert calculate_lit_pixels(instructions) == 6


TRUTH_END_STATE = dedent(
    """\
    .#..#.#
    #.#....
    .#....."""
)


def test_screen_state() -> None:
    s = Screen(width=7, height=3)
    s.run_sequence(SAMPLE_INPUT)
    assert str(s) == TRUTH_END_STATE
