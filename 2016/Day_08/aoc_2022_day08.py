import itertools
import re
import typing as t
from collections import defaultdict, deque, namedtuple
from enum import Enum
from pathlib import Path

from helpers.geometry import COORD


class InstructionType(Enum):  # noqa: D101
    RECT = 0
    ROTATE_COL = 1
    ROTATE_ROW = 2


Instruction = namedtuple("Instruction", ("instruction_type", "a", "b"))


def parse_instructions(sequence: str) -> list[Instruction]:
    """
    Parse the instruction provided into its component actions & parameters.

    The instruction is assumed to contain one of three sequences:
        * `rect AxB`
        * `rotate row y=A by B`
        * `rotate column x=A by B`
    """
    instructions = []
    for line in sequence.splitlines():
        if line.startswith("rect"):
            instruction_type = InstructionType.RECT
        elif line.startswith("rotate column"):
            instruction_type = InstructionType.ROTATE_COL
        elif line.startswith("rotate row"):
            instruction_type = InstructionType.ROTATE_ROW
        else:
            raise ValueError(f"Unsupported instruction: '{line}'")

        a, b, *_ = map(int, re.findall(r"\d+", line))
        instructions.append(Instruction(instruction_type, a, b))

    return instructions


def calculate_lit_pixels(instructions: t.Iterable[Instruction]) -> int:
    """Calculate the number of pixels that should be illuminated by the provided instructions."""
    # The only instruction that modifies pixel lighting is rect, and pixels will never be turned
    # off, so we can just calculate the number of pixels turned on by each rect instruction
    n_lit = 0
    for instruction in instructions:
        if instruction.instruction_type == InstructionType.RECT:
            n_lit += instruction.a * instruction.b

    return n_lit


class Screen:  # noqa: D101
    _state: dict[COORD, bool]

    def __init__(self, width: int = 50, height: int = 6) -> None:
        self.width = width
        self.height = height

        self._state = defaultdict(bool)

    def run_sequence(self, sequence: str) -> None:
        """
        Execute the provided screen instruction sequence.

        The instruction is assumed to contain one of three sequences:
            * `rect AxB`: turns on all of the pixels in a rectangle at the top-left of the screen
            which is `A` wide and `B` tall
            * `rotate row y=A by B`: shifts all of the pixels in row `A` right by `B` pixels,
            wrapping if necessary
            * `rotate column x=A by B`: shifts all of the pixels in column `A` down by `B` pixels,
            wrapping if necessary
        """
        instructions = parse_instructions(sequence)

        for instruction in instructions:
            if instruction.instruction_type == InstructionType.RECT:
                for coord in itertools.product(range(instruction.a), range(instruction.b)):
                    self._state[coord] = True
            elif instruction.instruction_type == InstructionType.ROTATE_COL:
                x, offset = instruction.a, instruction.b
                stash = deque(self._state[(x, y)] for y in range(self.height))
                stash.rotate(offset)
                for y, new_val in enumerate(stash):
                    self._state[(x, y)] = new_val

            elif instruction.instruction_type == InstructionType.ROTATE_ROW:
                y, offset = instruction.a, instruction.b
                stash = deque(self._state[(x, y)] for x in range(self.width))
                stash.rotate(offset)
                for x, new_val in enumerate(stash):
                    self._state[(x, y)] = new_val

    def __str__(self) -> str:
        rows = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                if self._state[(x, y)]:
                    row.append("#")
                else:
                    row.append(".")

            rows.append("".join(row))

        return "\n".join(rows)


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    print(f"Part One: {calculate_lit_pixels(parse_instructions(puzzle_input))}")

    s = Screen()
    s.run_sequence(puzzle_input)
    print(f"Part Two:\n{s}")
