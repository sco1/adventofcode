import math
from pathlib import Path


def parse_calibration_equations(raw_calibrations: str) -> list[tuple[int, list[int]]]:
    """
    Parse the provided bridge calibration equations into their components.

    Equations are assumed to be provided as newline delimited entries of the form `target: X Y Z`,
    where `X,Y,Z` are space delimited integers.
    """
    calibration_components = []  # Some target values may be repeated so don't use a dictionary
    for raw_cal in raw_calibrations.splitlines():
        raw_target, raw_components = raw_cal.split(":")
        calibration_components.append((int(raw_target), [int(c) for c in raw_components.split()]))

    return calibration_components


def can_solve(target: int, components: list[int], allow_concat: bool = False) -> bool:
    """
    Determine if the provided calibration is solvable by combining its components with operators.

    Allowed operators are addition and multiplication; if `allow_concat` is `True`, concatenation is
    added as a possible operator.

    NOTE: Operators are always evaluated left-to-right; operator precedence rules are ignored.
    """
    # This ends up being a surprisingly manageable recursion task.
    # For each pair of operators, chase the operator insertion tree down until we get to a final
    # value, then compare to the target.
    # Could probably optimize by assessing earlier whether or not the target is reachable,
    # but performance-wise this still manages part 2 in a few seconds so I'll leave it here for now
    if len(components) == 1:
        return target == components[0]

    if can_solve(target, [sum(components[:2])] + components[2:], allow_concat):
        return True

    if can_solve(target, [math.prod(components[:2])] + components[2:], allow_concat):
        return True

    if allow_concat:
        concat_args = int("".join(str(n) for n in components[:2]))
        if can_solve(target, [concat_args] + components[2:], allow_concat):
            return True

    return False


def calculate_calibration_result(
    calibration_components: list[tuple[int, list[int]]], allow_concat: bool = False
) -> int:
    """
    Calculate the total calibration result from the provided calibration equation components.

    The calibration result is calculated by summing the target calibration values for each solvable
    calibration equation.

    If `allow_concat` is `True`, the concatenation operator is allowed as a possible operator when
    attempting to solve the equation; otherwise only addition and multiplication are considered.
    """
    calibration_result = 0
    for target, components in calibration_components:
        if can_solve(target, components, allow_concat=allow_concat):
            calibration_result += target

    return calibration_result


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    calibration_components = parse_calibration_equations(puzzle_input)

    print(f"Part One: {calculate_calibration_result(calibration_components)}")
    print(f"Part Two: {calculate_calibration_result(calibration_components, True)}")
