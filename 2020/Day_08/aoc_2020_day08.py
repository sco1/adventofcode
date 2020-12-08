import itertools
import typing as t
from pathlib import Path


class RepeatInstructionError(RuntimeError):  # noqa: D101
    ...


class MaxIterExceeded(RuntimeError):  # noqa: D101
    ...


class Instruction(t.NamedTuple):  # noqa: D101
    op: t.Callable
    arg: int


class GameGear:
    """The handheld "intcode" machine for 2020 :'D."""

    instruction_set: list[Instruction]
    current_instruction: int
    accumulator: int

    _visited_instructions: set
    _n_steps: int
    _max_iter: int = 1_000_000

    def __init__(self, raw_instructions: str):
        self._ops = {  # There's probably a way to not do this every init but this is good enough
            "acc": self.acc,
            "jmp": self.jmp,
            "nop": self.nop,
        }

        self.instruction_set = self.parse_instructions(raw_instructions)
        self.reset()

    def reset(self) -> None:
        """Reset the machine to its power-on state."""
        self.current_instruction = 0
        self.accumulator = 0

        self._visited_instructions = set()
        self._n_steps = 0

    def acc(self, arg: int) -> None:
        """Increment the accumulator value by the given arg & step to the next instruction."""
        self.accumulator += arg
        self.current_instruction += 1

    def jmp(self, arg: int) -> None:
        """Jump to the instruction offset from the current by the provided arg."""
        self.current_instruction += arg

    def nop(self, *_: t.Any) -> None:
        """Do nothing & step to the next instruction."""
        self.current_instruction += 1

    def parse_instructions(self, raw_instructions: str) -> list[Instruction]:
        """Parse the provided instruction set into a series of Instructions for execution."""
        instruction_set = []
        for raw_instruction in raw_instructions.splitlines():
            op, arg = raw_instruction.split()
            instruction_set.append(Instruction(self._ops[op], int(arg)))

        return instruction_set

    def run(self) -> int:
        """
        Run the machine!

        Instructions will be executed until one of (hopefully) three conditions are met:
            * The end of the instructions is reached
            * Access to a specific instruction is repeated (raises `RepeatInstructionError`)
            * The total number of steps exceeds a configured threshold (raises `MaxIterExceeded`)
        """
        while True:
            # Reached the end of the instruction set
            if self.current_instruction >= len(self.instruction_set):
                return 1

            # Break out if we've reached a repeated instruction
            if self.current_instruction in self._visited_instructions:
                raise RepeatInstructionError(
                    f"Line {self.current_instruction}, Accumulator: {self.accumulator}"
                )

            # Just in case, prevent an actual infinite loop
            if self._n_steps > self._max_iter:
                raise MaxIterExceeded(f"{self._max_iter}")

            self._visited_instructions.add(self.current_instruction)
            instruction = self.instruction_set[self.current_instruction]
            instruction.op(instruction.arg)
            self._n_steps += 1


def mutate_until_fixed(initial_instructions: str) -> int:
    """
    Flip exactly one `jmp` to `nop` or vice-versa until the instructions run to completion.

    The provided instruction set is assumed to not successfuly run until completion.

    Per the problem statement, there should be exactly one flip necessary to ensure the program runs
    until completion.
    """
    instruction_lines = initial_instructions.splitlines()

    # For each line, try the flip if available & see if the machine runs to completion
    for idx, line in enumerate(instruction_lines):
        if line.startswith("nop"):
            new_line = line.replace("nop", "jmp")
        elif line.startswith("jmp"):
            new_line = line.replace("jmp", "nop")
        else:
            continue

        # chain tip via Ray Hettinger: https://twitter.com/raymondh/status/1335284170965221376
        new_instruction_set = "\n".join(
            itertools.chain(
                instruction_lines[:idx], [new_line], instruction_lines[idx + 1 :]  # noqa: E203
            )
        )

        machine = GameGear(new_instruction_set)
        try:
            status = machine.run()
        except (RepeatInstructionError, MaxIterExceeded):
            continue

        if status == 1:
            return machine.accumulator


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text()

    machine = GameGear(puzzle_input)
    try:
        machine.run()
    except RepeatInstructionError:
        pass

    print(f"Part One: Accumulator value at repeat is {machine.accumulator}")
    print(f"Part Two: Accumulator value at completion is {mutate_until_fixed(puzzle_input)}")
