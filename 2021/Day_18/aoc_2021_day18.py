import ast
import itertools
import math
import re
from pathlib import Path

PAIR = re.compile(r"\[(\d+),(\d+)\]")
TEN_PLUS = re.compile(r"\d\d+")
LEADING_NUM = re.compile(r"\d+(?!.*\d)")  # Match the rightmost number
NUM = re.compile(r"\d+")


def add_snailfish(left: str, right: str) -> str:
    """
    Perform snailfish addition.

    To add two snailfish numbers, form a pair from the left and right parameters of the addition
    operator. For example, `[1,2] + [[3,4],5]` becomes `[[1,2],[[3,4],5]]`.
    """
    return f"[{left},{right}]"


def _explode_pair(snailfish_number: str, pair: re.Match) -> str:
    """
    Explode the specified pair into its containing snailfish number.

    To explode a pair, the pair's left value is added to the first regular number to the left of the
    exploding pair (if any), and the pair's right value is added to the first regular number to the
    right of the exploding pair (if any). Then, the entire exploding pair is replaced with the
    regular number `0`.

    Exploding pairs will always consist of two regular numbers.
    """

    # Use nested replacement functions so they have the snailfish number & pair in scope
    def explode_left(match: re.Match) -> str:
        """Add the pair's left value to the first regular number to the left of the pair."""
        left = int(match[0])
        right = int(pair[1])
        return f"{left + right}"

    def explode_right(match: re.Match) -> str:
        """Add the pair's left value to the first regular number to the right of the pair."""
        left = int(match[0])
        right = int(pair[2])
        return f"{left + right}"

    head = snailfish_number[: pair.start()]
    exploded_head = LEADING_NUM.sub(explode_left, head, count=1)

    tail = snailfish_number[pair.end() :]
    exploded_tail = NUM.sub(explode_right, tail, count=1)

    return f"{exploded_head}0{exploded_tail}"


def _split_number(regular_number: re.Match | str) -> str:
    """
    Split the provided regular number.

    To split a regular number, replace it with a pair; the left element of the pair should be the
    regular number divided by two and rounded down, while the right element of the pair should be
    the regular number divided by two and rounded up.

    For example, `10` becomes `[5,5]`, `11` becomes `[5,6]`, `12` becomes `[6,6]`, and so on.
    """
    if isinstance(regular_number, re.Match):
        val = int(regular_number[0])
    else:
        val = int(regular_number)

    left = math.floor(val / 2)
    right = math.ceil(val / 2)

    return f"[{left},{right}]"


def _reduce(snailfish_number: str) -> str:
    """
    Reduce the provided snailfish number.

    To reduce a snailfish number, we repeatedly apply the first action in the following list that
    applies to the snailfish number:
        * If any pair is nested inside four pairs, the leftmost such pair explodes.
        * If any regular number is `10` or greater, the leftmost such regular number splits.

    During reduction, at most one action applies, after which the process returns to the top of the
    list of actions. For example, if split produces a pair that meets the explode criteria, that
    pair explodes before other splits occur.

    Once no action in the above list applies, the snailfish number is considered to be reduced.
    """
    while True:
        # Iterate over pairs to check for nesting levels
        to_top = False  # Sentinel to let us double break if we've exploded a pair
        for pair in PAIR.finditer(snailfish_number):
            head = snailfish_number[: pair.start()]
            nesting_level = head.count("[") - head.count("]")
            if nesting_level >= 4:
                # If we're 4 or more layers deep then the pair needs to be exploded
                snailfish_number = _explode_pair(snailfish_number, pair)
                to_top = True
                break

        if to_top:
            # At most one action per loop
            continue

        # Check for values that are greater or equal to 10 that need to be split
        split_check = TEN_PLUS.search(snailfish_number)
        if split_check:
            snailfish_number = TEN_PLUS.sub(_split_number, snailfish_number, count=1)
            continue

        # If we've gotten here then we should be fully reduced
        return snailfish_number


def calculate_sum(snailfish_numbers: list[str]) -> str:
    """Calculate the sum of the provided list of snailfish numbers."""
    running_sum = snailfish_numbers[0]
    for next_num in snailfish_numbers[1:]:
        running_sum = _reduce(add_snailfish(running_sum, next_num))

    return running_sum


def _calculate_value(component: int | list) -> int:
    """
    Recursively calculate the value of the provided component.

    Components are assumed to be either a regular number (`int`) or a snailfish number pair, which
    may be arbitrarily nested. The magnitude of a pair is 3 times the magnitude of its left element
    plus 2 times the magnitude of its right element.
    """
    if isinstance(component, int):
        return component

    return (3 * _calculate_value(component[0])) + (2 * _calculate_value(component[1]))


def calculate_magnitude(snailfish_number: str) -> int:
    """
    Calculate the magnitude of the provided snailfish number.

    The magnitude of a pair is 3 times the magnitude of its left element plus 2 times the magnitude
    of its right element. The magnitude of a regular number is just that number. Magnitude
    calculations are recursive.

    The provided snailfish number string is assumed to be safely eval-able into a list.
    """
    # Use literal_eval to listify the input & enter the recursive sum calculation
    return _calculate_value(ast.literal_eval(snailfish_number))


def largest_magnitude(snailfish_numbers: list[str]) -> int:
    """
    Calculate the largest magnitude one can get from adding only two of the snailfish numbers.

    NOTE: Snailfish addition is not commutative - `x + y` and `y + x` can produce different results.
    """
    maximum = 0
    for left, right in itertools.combinations(snailfish_numbers, 2):
        maximum = max(
            (
                maximum,
                # Since addition isn't commutative, we have to check both sides
                calculate_magnitude(_reduce(add_snailfish(left, right))),
                calculate_magnitude(_reduce(add_snailfish(right, left))),
            )
        )

    return maximum


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().splitlines()

    summation = calculate_sum(puzzle_input)
    print(f"Part One: {calculate_magnitude(summation)}")
    print(f"Part Two: {largest_magnitude(puzzle_input)}")
