from pathlib import Path


def solve_captcha(captcha: str, use_half_jump: bool = False) -> int:
    """
    Solve the provided capcha to prove that we're not a human.

    If `use_half_jump` is `False`, the captcha is calculated by finding the sum of all digits that
    match the next digit in the list. Otherwise, the captcha is calculated by finding the sum of all
    digits that match the digit halfway around the circular list. e.g. if the

    NOTE: The list is treated as circular, so the digit after the last digit is the first digit in
    the list.

    NOTE: The input captcha is assumed to have an even number of elements.
    """
    digits = [int(char) for char in captcha]

    if use_half_jump:
        step = len(digits) // 2
    else:
        step = 1

    out_sum = 0
    for idx, digit in enumerate(digits):
        if digit == digits[(idx + step) % len(digits)]:
            out_sum += digit

    return out_sum


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    print(f"Part One: {solve_captcha(puzzle_input)}")
    print(f"Part Two: {solve_captcha(puzzle_input, use_half_jump=True)}")
