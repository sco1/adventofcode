from textwrap import dedent

import pytest

from .aoc_2022_day05 import (
    Instruction,
    _parse_instructions,
    _parse_stack_map,
    parse_puzzle_input,
    run_instructions,
)

SAMPLE_STACKS = (
    (
        dedent(
            """\
                [D]
            [N] [C]
            [Z] [M] [P]
             1   2   3
            """
        ),
        [["Z", "N"], ["M", "C", "D"], ["P"]],
    ),
    (
        dedent(
            """\
                    [Z]
                    [N]
            [M]     [D]
            [C]     [P]
             1   2   3
            """
        ),
        [["C", "M"], [], ["P", "D", "N", "Z"]],
    ),
)


@pytest.mark.parametrize(("stack_map", "truth_stacks"), SAMPLE_STACKS)
def test_stack_parse(stack_map: str, truth_stacks: list[list[str]]) -> None:
    assert _parse_stack_map(stack_map) == truth_stacks


SAMPLE_INSTRUCTIONS = dedent(
    """\
    move 1 from 2 to 1
    move 3 from 1 to 3
    """
)


def test_instruction_parse() -> None:
    assert _parse_instructions(SAMPLE_INSTRUCTIONS) == [Instruction(1, 1, 0), Instruction(3, 0, 2)]


SAMPLE_INPUT = dedent(
    """\
        [D]
    [N] [C]
    [Z] [M] [P]
     1   2   3

    move 1 from 2 to 1
    move 3 from 1 to 3
    move 2 from 2 to 1
    move 1 from 1 to 2
    """
)


def test_instruction_execute() -> None:
    stacks, instructions = parse_puzzle_input(SAMPLE_INPUT)
    assert run_instructions(stacks, instructions) == "CMZ"


def test_instruction_execute_newcrane() -> None:
    stacks, instructions = parse_puzzle_input(SAMPLE_INPUT)
    assert run_instructions(stacks, instructions, is_new_crane=True) == "MCD"
