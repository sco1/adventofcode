import copy
import re
import typing as t
from pathlib import Path

STACK_MAP: t.TypeAlias = list[list[str]]

INSTRUCTION_RE = re.compile(r"move (\d+) from (\d)+ to (\d+)")


class Instruction(t.NamedTuple):  # noqa: D101
    n: int
    source: int
    dest: int


def _parse_stack_map(stack_map: str) -> STACK_MAP:
    """
    Parse the provided stack map into a collection of stacks to work with the crane.

    Inputs are assumed to be of the form:
            [D]
        [N] [C]
        [Z] [M] [P]
         1   2   3

    Where the width of each stack is 3 characters & the final line is the (1-based) stack index.

    Stacks are mapped bottom -> top, e.g. Stack 1 in the above example would be mapped as
    `["Z", "N"]`.
    """
    *rows, stack_idx = stack_map.splitlines()
    n_stacks = int(stack_idx.split()[-1])

    stacks: list[list[str]] = [[] for _ in range(n_stacks)]
    for row in reversed(rows):  # Reverse so we're popping/appending on the right later on
        for idx, char in enumerate(row[1::4]):
            if char.strip():
                stacks[idx].append(char)

    return stacks


def _parse_instructions(instructions: str) -> list[Instruction]:
    """
    Parse the provided crane operator instructions.

    Inputs are assumed to be of the form: `"move 1 from 2 to 1"`, which translates to "move 1 crate
    from stack 2 to stack 1".

    Input stack indices are 1-indexed, and are transformed to 0-indexed for the final output.
    """
    parsed_instructions = []
    for line in instructions.splitlines():
        if instruction := INSTRUCTION_RE.match(line):
            n, source, dest = (int(val) for val in instruction.groups())
            # Stacks are 1-indexed in the instructions so we need to adjust their indices
            parsed_instructions.append(Instruction(n, source - 1, dest - 1))

    return parsed_instructions


def parse_puzzle_input(puzzle_input: str) -> tuple[STACK_MAP, list[Instruction]]:
    """Parse the provided puzzle input into its component stack map and operator instructions."""
    stack_map, instructions = puzzle_input.split("\n\n")

    stacks = _parse_stack_map(stack_map)
    parsed_instructions = _parse_instructions(instructions)

    return stacks, parsed_instructions


def run_instructions(
    stack_map: STACK_MAP, instructions: list[Instruction], is_new_crane: bool = False
) -> str:
    """
    Have the crane operator run the provided instructions on the crate stack.

    If `is_new_crane` is `True`, the operator is using a CrateMover 9001, which can move multiple
    crates at once. Otherwise, the operator is using a CrateMover 9000, which can only move one
    crate at a time.
    """
    if is_new_crane:
        for instruction in instructions:
            stack_map[instruction.dest].extend(stack_map[instruction.source][-instruction.n : :])

            for _ in range(instruction.n):
                stack_map[instruction.source].pop()
    else:
        for instruction in instructions:
            for _ in range(instruction.n):
                stack_map[instruction.dest].append(stack_map[instruction.source].pop())

    return "".join(stack[-1] for stack in stack_map)


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text()

    stacks, instructions = parse_puzzle_input(puzzle_input)

    # Use deep copies since we're mutating the stacks
    print(f"Part One: {run_instructions(copy.deepcopy(stacks), instructions)}")
    print(f"Part Two: {run_instructions(copy.deepcopy(stacks), instructions, is_new_crane=True)}")
