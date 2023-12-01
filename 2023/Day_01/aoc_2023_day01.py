from pathlib import Path

DIGIT_WORDS = (
    ("one", "1"),
    ("two", "2"),
    ("three", "3"),
    ("four", "4"),
    ("five", "5"),
    ("six", "6"),
    ("seven", "7"),
    ("eight", "8"),
    ("nine", "9"),
)


def extract_calibration_value(calibration_string: str, include_spelled: bool = False) -> int:
    """
    Extract the calibration value from the provided calibration string.

    The calibration value can be found by combining the first digit and the last digit to form a
    single two-digit number.

    If `include_spelled` is `True`, valid digits may also be spelled out, e.g. `"one" = 1`,
    `"two" = 2`, etc.

    NOTE: Compound numbers may contain valid digits, e.g. `"sixteen" = 6`
    NOTE: Characters are not consumed as they match, e.g. `"twone"` gives `2` and `1`.
    """
    digits = []
    for idx, c in enumerate(calibration_string):
        if c.isdigit():
            digits.append(c)
            continue

        if include_spelled:
            # Roll through the rest of the characters in the line to see if they match a word
            # This keeps us from consuming letters like using a buffer would
            for word, digit in DIGIT_WORDS:
                if calibration_string[idx:].startswith(word):
                    digits.append(digit)
                    break

    if not digits:
        raise ValueError(f"Could not locate any digits from string '{calibration_string}'")
    elif len(digits) == 1:
        digit_str = f"{digits[0]*2}"
    else:
        digit_str = f"{digits[0]}{digits[-1]}"

    return int(digit_str)


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    print(f"Part One: {sum(extract_calibration_value(cal) for cal in puzzle_input.splitlines())}")
    print(
        f"Part Two: {sum(extract_calibration_value(cal, include_spelled=True) for cal in puzzle_input.splitlines())}"  # noqa: E501
    )
