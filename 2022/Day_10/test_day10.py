from collections import deque
from pathlib import Path
from textwrap import dedent

from .aoc_2022_day10 import debug_register, render_image

SAMPLE_INPUT = Path("./sample_input.txt").read_text().splitlines()


def test_part_one() -> None:
    QUERY_CYCLES = deque((20, 60, 100, 140, 180, 220))
    assert sum(debug_register(SAMPLE_INPUT, QUERY_CYCLES)) == 13140


SAMPLE_IMAGE = dedent(
    """\
    ##..##..##..##..##..##..##..##..##..##..
    ###...###...###...###...###...###...###.
    ####....####....####....####....####....
    #####.....#####.....#####.....#####.....
    ######......######......######......####
    #######.......#######.......#######....."""
)


def test_part_two() -> None:
    assert render_image(SAMPLE_INPUT) == SAMPLE_IMAGE
