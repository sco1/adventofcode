from textwrap import dedent

import pytest

from .aoc_2024_day07 import calculate_calibration_result, can_solve, parse_calibration_equations

SAMPLE_INPUT = dedent(
    """\
    190: 10 19
    3267: 81 40 27
    83: 17 5
    156: 15 6
    7290: 6 8 6 15
    161011: 16 10 13
    192: 17 8 14
    21037: 9 7 18 13
    292: 11 6 16 20
    """
)

TRUTH_PARSED = [
    (190, [10, 19]),
    (3267, [81, 40, 27]),
    (83, [17, 5]),
    (156, [15, 6]),
    (7290, [6, 8, 6, 15]),
    (161011, [16, 10, 13]),
    (192, [17, 8, 14]),
    (21037, [9, 7, 18, 13]),
    (292, [11, 6, 16, 20]),
]


def test_parse_calibration_equations() -> None:
    assert parse_calibration_equations(SAMPLE_INPUT) == TRUTH_PARSED


SOLVABLE_CASES = (
    (190, [10, 19], True),
    (3267, [81, 40, 27], True),
    (83, [17, 5], False),
    (156, [15, 6], False),
    (7290, [6, 8, 6, 15], False),
    (161011, [16, 10, 13], False),
    (192, [17, 8, 14], False),
    (21037, [9, 7, 18, 13], False),
    (292, [11, 6, 16, 20], True),
)


@pytest.mark.parametrize(("target", "components", "truth_solvable"), SOLVABLE_CASES)
def test_can_solve(target: int, components: list[int], truth_solvable: bool) -> None:
    assert can_solve(target, components) == truth_solvable


def test_calibration_result() -> None:
    calibration_components = parse_calibration_equations(SAMPLE_INPUT)
    assert calculate_calibration_result(calibration_components) == 3749


SOLVABLE_CASES_WITH_CONCAT = (
    (190, [10, 19], True),
    (3267, [81, 40, 27], True),
    (83, [17, 5], False),
    (156, [15, 6], True),
    (7290, [6, 8, 6, 15], True),
    (161011, [16, 10, 13], False),
    (192, [17, 8, 14], True),
    (21037, [9, 7, 18, 13], False),
    (292, [11, 6, 16, 20], True),
)


@pytest.mark.parametrize(("target", "components", "truth_solvable"), SOLVABLE_CASES_WITH_CONCAT)
def test_can_solve_with_concat(target: int, components: list[int], truth_solvable: bool) -> None:
    assert can_solve(target, components, allow_concat=True) == truth_solvable


def test_calibration_result_with_concat() -> None:
    calibration_components = parse_calibration_equations(SAMPLE_INPUT)
    assert calculate_calibration_result(calibration_components, allow_concat=True) == 11_387
