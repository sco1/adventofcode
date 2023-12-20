from textwrap import dedent

import pytest

from helpers.geometry import MoveDir
from .aoc_2023_day18 import Instruction, dig_trench, parse_dig_instructions

SAMPLE_INPUT = dedent(
    """\
    R 6 (#70c710)
    D 5 (#0dc571)
    L 2 (#5713f0)
    D 2 (#d2c081)
    R 2 (#59c680)
    D 2 (#411b91)
    L 5 (#8ceee2)
    U 2 (#caa173)
    L 1 (#1b58a2)
    U 2 (#caa171)
    R 2 (#7807d2)
    U 3 (#a77fa3)
    L 2 (#015232)
    U 2 (#7a21e3)
    """
)
INSTRUCTIONS = parse_dig_instructions(SAMPLE_INPUT)


def test_trench_dig() -> None:
    assert dig_trench(INSTRUCTIONS, fill=False) == 38


def test_trench_fill() -> None:
    assert dig_trench(INSTRUCTIONS, fill=True) == 62


COLOR_CODE_CASES = (
    ("#70c710", Instruction(MoveDir.EAST, 46_1937, "#70c710")),
    ("#0dc571", Instruction(MoveDir.SOUTH, 56_407, "#0dc571")),
    ("#5713f0", Instruction(MoveDir.EAST, 356_671, "#5713f0")),
    ("#d2c081", Instruction(MoveDir.SOUTH, 863_240, "#d2c081")),
    ("#59c680", Instruction(MoveDir.EAST, 367_720, "#59c680")),
    ("#411b91", Instruction(MoveDir.SOUTH, 266_681, "#411b91")),
    ("#8ceee2", Instruction(MoveDir.WEST, 577_262, "#8ceee2")),
    ("#caa173", Instruction(MoveDir.NORTH, 829_975, "#caa173")),
    ("#1b58a2", Instruction(MoveDir.WEST, 112_010, "#1b58a2")),
    ("#caa171", Instruction(MoveDir.SOUTH, 829_975, "#caa171")),
    ("#7807d2", Instruction(MoveDir.WEST, 491_645, "#7807d2")),
    ("#a77fa3", Instruction(MoveDir.NORTH, 686_074, "#a77fa3")),
    ("#015232", Instruction(MoveDir.WEST, 5_411, "#015232")),
    ("#7a21e3", Instruction(MoveDir.NORTH, 500_254, "#7a21e3")),
)


@pytest.mark.parametrize(("color_code", "truth_instruction"), COLOR_CODE_CASES)
def test_color_conversion(color_code: str, truth_instruction: Instruction) -> None:
    assert Instruction.from_color(color_code) == truth_instruction


def test_translated_color() -> None:
    assert dig_trench(INSTRUCTIONS, translate_color=True) == 952_408_144_115
