import operator
from functools import reduce
from itertools import product
from math import ceil
from pathlib import Path
from typing import List, Optional


class IntcodeMachine:
    """Represent our Intcode computer & its operations."""

    def __init__(
        self,
        in_program: List[int],
        noun: Optional[int] = None,
        verb: Optional[int] = None,
        processing_chunk_size: int = 4,
    ):
        self.OPCODES = {1: self.oper_add, 2: self.oper_mul}

        self._in_program = tuple(in_program)  # Keep an immutable copy for reference
        self._processing_chunk_size = processing_chunk_size

        self.reset_memory(noun, verb)

    @property
    def output(self) -> int:
        """Return the machine's output, as stored at address 0 of the processed program."""
        return self.program[0]

    def sub_noun_verb(self) -> None:
        """Replace values at addresses 1 & 2 if overrides are provided, otherwise do not change."""
        if self.noun:
            self.program[1] = self.noun

        if self.verb:
            self.program[2] = self.verb

    def reset_memory(self, noun: Optional[int] = None, verb: Optional[int] = None) -> None:
        """Reset the machine's memory to the original input, update the noun & verb, and process."""
        self.program = list(self._in_program)
        self.noun = noun
        self.verb = verb

        self.sub_noun_verb()
        self.process_opcode()

    def process_opcode(self) -> None:
        """Iterate over opcode chunks & dispatch the relevant values to the opcode operators."""
        # Iterate over discrete chunks so we don't worry about modifying what we're iterating over.
        n_steps = ceil(len(self._in_program) / self._processing_chunk_size)
        for i in range(n_steps):
            program_chunk = self.program[
                i * self._processing_chunk_size : self._processing_chunk_size * (i + 1)
            ]
            opcode = program_chunk[0]

            # End processing on opcode 99
            if opcode == 99:
                return

            try:
                oper_values = [self.program[idx] for idx in program_chunk[1:-1]]
                place_address = program_chunk[-1]
                self.OPCODES[opcode](oper_values, place_address)
            except KeyError:
                raise ValueError(f"Unknown opcode: {opcode}")

    def oper_add(self, oper_values: List[int], place_idx: int) -> None:
        """Sum the input values & place them at the specified index in the full opcode."""
        self.program[place_idx] = sum(oper_values)

    def oper_mul(self, oper_values: List[int], place_idx: int) -> None:
        """Multiply the input values & place them at the specified index in the full opcode."""
        self.program[place_idx] = reduce(operator.mul, oper_values)

    @classmethod
    def find_noun_verb(
        cls, in_program: List[int], target_output: int, max_noun_verb: int = 99
    ) -> Optional["IntcodeMachine"]:
        """From the starting program, iterate over noun & verb until desired output is reached."""
        machine = cls(in_program)
        for noun, verb in product(range(max_noun_verb + 1), repeat=2):
            # Short-circuit if the noun or verb provides an unreachable instruction address
            if noun >= len(machine.program) or verb >= len(machine.program):
                continue

            machine.reset_memory(noun, verb)
            if machine.output == target_output:
                return machine
        else:
            # No valid machine found
            return


if __name__ == "__main__":
    puzzle_input = Path("./puzzle_input.txt")

    with puzzle_input.open("r") as f:
        in_program = [int(code) for code in f.read().strip().split(",")]

    # Part 1
    part_one_machine = IntcodeMachine(in_program, noun=12, verb=2)
    print(part_one_machine.output)

    # Part 2
    part_two_machine = IntcodeMachine.find_noun_verb(in_program, 19690720)
    print(100 * part_two_machine.noun + part_two_machine.verb)
