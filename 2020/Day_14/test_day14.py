from textwrap import dedent

from .aoc_2020_day14 import FerryComputer

SAMPLE_PROGRAM = dedent(
    """\
    mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
    mem[8] = 11
    mem[7] = 101
    mem[8] = 0
    """
)


def test_part_one() -> None:  # noqa: D103
    computer = FerryComputer(SAMPLE_PROGRAM)
    computer.run_program()

    assert computer.initialization_value == 165


PART_TWO_SAMPLE = dedent(
    """\
    mask = 000000000000000000000000000000X1001X
    mem[42] = 100
    mask = 00000000000000000000000000000000X0XX
    mem[26] = 1
    """
)


def test_part_two() -> None:  # noqa: D103
    computer = FerryComputer(PART_TWO_SAMPLE, is_v2=True)
    computer.run_program()

    assert computer.initialization_value == 208
