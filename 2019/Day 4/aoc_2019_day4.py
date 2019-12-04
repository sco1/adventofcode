from itertools import groupby
from pathlib import Path
from typing import List, Tuple, Union


def run_length_endcode(in_str: str) -> List[Tuple[str, int]]:
    """Generate the RLE of the input string of single-digit integers as a list of tuple."""
    return [(digit, sum(1 for i in subgroup)) for digit, subgroup in groupby(in_str)]


def is_valid_password(password: Union[int, str], strict: bool = False) -> bool:
    """
    Determine validity of the password, as int or str of int, based on the provided ruleset.

    Validity check is based on the following:
        * It is a six-digit number
        * Has at least one set of two equal adjacent digits
        * Going from left to right, the digits never only increase or stay the same
        * (`strict` only) At least one of the pair of adjacent matching digits is not part of a
          larger group of matching digits
    """
    if isinstance(password, int):
        # Convert to str for easier iteration
        password = str(password)

    # Short-circuit check for password length
    if len(password) != 6:
        return False

    password_rle = run_length_endcode(password)
    # Short-circuit check for descending values
    password_rle_order = [group[0] for group in password_rle]
    if sorted(password_rle_order) != password_rle_order:
        return False

    if not strict:
        # Valid password has at least one run of > 2 digits
        return any(run >= 2 for _, run in password_rle)
    else:
        # Valid password has at least one run of exactly 2 digits
        return any(run == 2 for _, run in password_rle)


def find_valid_passwords(range_start: int, range_end: int, strict: bool = False) -> List[int]:
    """Generate a list of valid passwords given the criteria for Part Two."""
    return [
        password
        for password in range(range_start, range_end + 1)
        if is_valid_password(password, strict)
    ]


if __name__ == "__main__":
    puzzle_input = Path("./puzzle_input.txt")

    with puzzle_input.open("r") as f:
        range_start, range_end = [int(num) for num in f.read().strip().split("-")]

    # Part 1
    print(len(find_valid_passwords(range_start, range_end)))

    # Part 2
    print(len(find_valid_passwords(range_start, range_end, strict=True)))
