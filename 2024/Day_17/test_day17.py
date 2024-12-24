from textwrap import dedent

from .aoc_2024_day17 import ChronoComp

SAMPLE_INPUT = dedent(
    """\
    Register A: 729
    Register B: 0
    Register C: 0

    Program: 0,1,5,4,3,0
    """
)
TRUTH_STDOUT = "4,6,3,5,6,3,5,2,1,0"


def test_chrono_prog() -> None:
    ccomp = ChronoComp.from_debug(SAMPLE_INPUT)
    ccomp.run()

    assert ccomp.stdout == TRUTH_STDOUT


def test_prog_a() -> None:
    ccomp = ChronoComp(registers={"A": 0, "B": 0, "C": 9}, program=(2, 6))
    ccomp.run()

    assert ccomp.registers["B"] == 1


def test_prog_b() -> None:
    ccomp = ChronoComp(registers={"A": 10, "B": 0, "C": 0}, program=(5, 0, 5, 1, 5, 4))
    ccomp.run()

    assert ccomp.stdout == "0,1,2"


def test_prog_c() -> None:
    ccomp = ChronoComp(registers={"A": 2024, "B": 0, "C": 0}, program=(0, 1, 5, 4, 3, 0))
    ccomp.run()

    assert ccomp.registers["A"] == 0
    assert ccomp.stdout == "4,2,5,6,7,7,7,7,3,1,0"


def test_prog_d() -> None:
    ccomp = ChronoComp(registers={"A": 0, "B": 29, "C": 0}, program=(1, 7))
    ccomp.run()

    assert ccomp.registers["B"] == 26


def test_prog_e() -> None:
    ccomp = ChronoComp(registers={"A": 0, "B": 2024, "C": 43_690}, program=(4, 0))
    ccomp.run()

    assert ccomp.registers["B"] == 44_354
