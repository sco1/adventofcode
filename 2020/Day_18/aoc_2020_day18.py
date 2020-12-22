import operator
import typing as t
from collections import deque
from pathlib import Path

# Per the puzzle description, we only have to worry about 2 operators
OPS = {
    "+": operator.add,
    "*": operator.mul,
}


def parse_equation(equation: str) -> t.Deque:
    """
    Parse the provided equation into a deque for processing.

    NOTE: For simplicity, values are assumed to be single-digit integers.
    """
    # Remove spaces & create a deque for scanning the equation from left-to-right
    equation = equation.replace(" ", "")
    equation_dq = deque((int(char) if char.isdigit() else char) for char in equation)

    return equation_dq


def parenthesizer(equation: str) -> str:
    """
    Transform the provided equation so it mimics following the advanced math operator precedence.

    For advanced math, addition is evaluated before multiplication.
    """
    # To fake the new operator precedence without actually doing operator precedence in the
    # calculation function, we can add layers of parentheses into the equation to adjust contexts
    # in order to get the precedence we want
    new_equation = ["(("]  # Assume equations start with an integer

    for char in equation:
        # Parentheses still have highest precedence, so they become the deepest scope
        if char == "(":
            new_equation.append("(((")
        elif char == ")":
            new_equation.append(")))")
        # Addition has higher precedence than multiplication, so its scope sits on top
        elif char == "+":
            new_equation.append(")+(")
        elif char == "*":
            new_equation.append("))*((")
        # Otherwise, we have the digits
        else:
            new_equation.append(char)

    new_equation.append("))")
    return "".join(new_equation)


def run_calc(equation: t.Deque) -> int:
    """
    Execute the equation & provide the calculated value.

    Equations are executed from left-to-right; only parentheses are given precedence.

    NOTE: For simplicity, values are assumed to be single-digit integers.
    """
    output = None
    op = None

    while equation:
        step = equation.popleft()

        # For parentheses, use recursion to evaluate in their own context
        if step == "(":
            if output is None:
                # If the equation opens with a parentheses, we can jump straight in
                output = run_calc(equation)
            else:
                # Otherwise, we can assume that we've encountered a value and operator
                # e.g. we can't have things like "*(2 + 5)"
                output = op(output, run_calc(equation))
        elif step == ")":
            # Exiting out of the equation context
            return output
        elif isinstance(step, int):
            if output is None:
                # First value encounter
                output = step
            else:
                # Otherwise, we can assume we've encountered an operator
                output = op(output, step)
        else:
            # If we've gotten here, then we probably have an operator
            op = OPS[step]

    return output


def calc_equation(equation: str, is_advanced_math: bool = False) -> int:
    """
    Helper function to run the calculation for a single equation.

    If the `is_advanced_math` flag is `True` then the equation is transformed such that addition
    has a higher precedence than multiplication.
    """
    if is_advanced_math:
        equation = parenthesizer(equation)

    return run_calc(parse_equation(equation))


def calc_all_homework(homework: str, is_advanced_math: bool = False) -> int:
    """
    Helper function to run the calculation for the entire set of homework equations.

    If the `is_advanced_math` flag is `True` then the equation is transformed such that addition
    has a higher precedence than multiplication.
    """
    return sum(calc_equation(line, is_advanced_math) for line in homework.splitlines())


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text()

    print(f"Part One: {calc_all_homework(puzzle_input)}")
    print(f"Part Two: {calc_all_homework(puzzle_input, is_advanced_math=True)}")
