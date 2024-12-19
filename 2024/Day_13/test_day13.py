from textwrap import dedent

import pytest

from .aoc_2024_day13 import Button, ClawMachine, Prize, parse_machine_spec

SAMPLE_INPUT = dedent(
    """\
    Button A: X+94, Y+34
    Button B: X+22, Y+67
    Prize: X=8400, Y=5400

    Button A: X+26, Y+66
    Button B: X+67, Y+21
    Prize: X=12748, Y=12176

    Button A: X+17, Y+86
    Button B: X+84, Y+37
    Prize: X=7870, Y=6450

    Button A: X+69, Y+23
    Button B: X+27, Y+71
    Prize: X=18641, Y=10279
    """
)


def test_machine_parse() -> None:
    raw_spec = dedent(
        """\
        Button A: X+94, Y+34
        Button B: X+22, Y+67
        Prize: X=8400, Y=5400
        """
    )

    truth_machine = ClawMachine(a=Button(94, 34), b=Button(22, 67), prize=Prize(8400, 5400))

    assert ClawMachine.from_raw(raw_spec) == truth_machine


def test_parse_machine_multi() -> None:
    truth_specs = [
        ClawMachine(a=Button(94, 34), b=Button(22, 67), prize=Prize(8400, 5400)),
        ClawMachine(a=Button(26, 66), b=Button(67, 21), prize=Prize(12748, 12176)),
        ClawMachine(a=Button(17, 86), b=Button(84, 37), prize=Prize(7870, 6450)),
        ClawMachine(a=Button(69, 23), b=Button(27, 71), prize=Prize(18641, 10279)),
    ]

    assert parse_machine_spec(SAMPLE_INPUT) == truth_specs


SOLVABLE_TEST_CASES = (
    (ClawMachine(a=Button(94, 34), b=Button(22, 67), prize=Prize(8400, 5400)), (80, 40)),
    (ClawMachine(a=Button(26, 66), b=Button(67, 21), prize=Prize(12748, 12176)), None),
    (ClawMachine(a=Button(17, 86), b=Button(84, 37), prize=Prize(7870, 6450)), (38, 86)),
    (ClawMachine(a=Button(69, 23), b=Button(27, 71), prize=Prize(18641, 10279)), None),
)


@pytest.mark.parametrize(("claw_machine", "truth_presses"), SOLVABLE_TEST_CASES)
def test_solve_machine(claw_machine: ClawMachine, truth_presses: tuple[int, int]) -> None:
    assert claw_machine.calculate_prize_presses() == truth_presses


TOKEN_COST_TEST_CASES = (
    (ClawMachine(a=Button(94, 34), b=Button(22, 67), prize=Prize(8400, 5400)), 280),
    (ClawMachine(a=Button(26, 66), b=Button(67, 21), prize=Prize(12748, 12176)), None),
    (ClawMachine(a=Button(17, 86), b=Button(84, 37), prize=Prize(7870, 6450)), 200),
    (ClawMachine(a=Button(69, 23), b=Button(27, 71), prize=Prize(18641, 10279)), None),
)


@pytest.mark.parametrize(("claw_machine", "truth_cost"), TOKEN_COST_TEST_CASES)
def test_token_cost(claw_machine: ClawMachine, truth_cost: int) -> None:
    assert claw_machine.winning_token_cost() == truth_cost
