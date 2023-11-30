import typing as t
from pathlib import Path
from textwrap import dedent

COORD: t.TypeAlias = tuple[int, int]

KEYPAD = dedent(
    """\
    123
    456
    789"""
)

DIAMOND_KEYPAD = dedent(
    """\
      1
     234
    56789
     ABC
      D"""
)

DELTA = {
    "U": (0, -1),
    "D": (0, 1),
    "L": (-1, 0),
    "R": (1, 0),
}


def parse_keypad(raw_keypad: str = KEYPAD, start_val: str = "5") -> tuple[dict[COORD, str], COORD]:
    """
    Parse the provided keypad description into a coordinate index of its buttons.

    The coordinate location of `start_val` is also optionally returned for later use.
    """
    key_locs: dict[COORD, str] = {}
    start_loc = (-1, -1)
    for y, row in enumerate(raw_keypad.splitlines()):
        for x, c in enumerate(row):
            if c.strip():
                key_locs[(x, y)] = c

                if c == start_val:
                    start_loc = (x, y)

    return key_locs, start_loc


def find_bathroom_code(instructions: str, keypad: dict[COORD, str], start_loc: COORD) -> str:
    """
    Follow the instructions to determine the code to enter on the keypad to enter the bathroom.

    The bathroom code is composed of the digits at the location reached at the end of each line; in
    other words if the instructions have `n` lines the code is `n` digits long.

    The instructions are assumed to be provided as a series of `UDLR` instructions describing the
    shift from the previous location. If a location cannot be reached, the instruction is skipped.
    The instructions begin at the location of the `5` button; this position does not reset at the
    end of each line of instruction.
    """
    code_digits = []
    x, y = start_loc
    for digit_line in instructions.splitlines():
        for move in digit_line:
            dx, dy = DELTA[move]
            (nx, ny) = (x + dx, y + dy)

            if (nx, ny) in keypad:
                x, y = nx, ny

        code_digits.append(keypad[(x, y)])

    return "".join(code_digits)


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    regular_keypad, start_loc = parse_keypad()
    print(f"Part One: {find_bathroom_code(puzzle_input, regular_keypad, start_loc)}")

    diamond_keypad, start_loc = parse_keypad(DIAMOND_KEYPAD)
    print(f"Part Two: {find_bathroom_code(puzzle_input, diamond_keypad, start_loc)}")
