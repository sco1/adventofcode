from textwrap import dedent

from .aoc_2020_day08 import GameGear, RepeatInstructionError, mutate_until_fixed

SAMPLE_INSTRUCTIONS = dedent(
    """\
    nop +0
    acc +1
    jmp +4
    acc +3
    jmp -3
    acc -99
    acc +1
    jmp -4
    acc +6
    """
)

MACHINE = GameGear(SAMPLE_INSTRUCTIONS)


def test_infinite_loop_termination() -> None:
    """Test for correct accumulator value after machine reaches its first repeated instruction."""
    MACHINE.reset()

    try:
        MACHINE.run()
    except RepeatInstructionError:
        pass

    assert MACHINE.accumulator == 5


def test_corruption_fixing() -> None:
    """Test that the machine is correctly fixed & runs the instruction set to completion."""
    assert mutate_until_fixed(SAMPLE_INSTRUCTIONS) == 8
