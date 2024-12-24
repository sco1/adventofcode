from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import IntEnum
from pathlib import Path


class OpCode(IntEnum):  # noqa: D101
    ADV = 0
    BXL = 1
    BST = 2
    JNZ = 3
    BXC = 4
    OUT = 5
    BDV = 6
    CDV = 7


class HaltError(Exception): ...  # noqa: D101


@dataclass(slots=True)
class ChronoComp:
    """
    Welcome to the Chronospatial Computer!

    The Chronospatial Computer is a 3-bit computer with 3 registers: `A`, `B`, and `C`. This
    computer knows eight instructions, each identified by a 3-bit number (opcode), enumerated by
    `OpCode`. Each instruction also reads the 3-bit number after it as an input (operand).

    An instruction pointer identifies the position in the program from which the next opcode will be
    read; it starts at `0`, pointing at the first 3-bit number in the program. Except for jump
    instructions, the instruction pointer increases by `2` after each instruction is processed (to
    move past the instruction's opcode and its operand). If the computer tries to read an opcode
    past the end of the program, it instead halts.

    Outputs are written to `stdout`; if a program outputs multiple values they are separated by
    commas.
    """

    registers: dict[str, int]
    program: tuple[int, ...]

    _pointer: int = 0

    _stdout: list[int] = field(default_factory=list)

    def read(self) -> int:
        """
        Read the value at the current instruction pointer & advance the pointer by 1.

        If attempting to read past the end of the program, a `HaltError` is raised instead.
        """
        try:
            val = self.program[self._pointer]
            self._pointer += 1
        except IndexError:
            raise HaltError from None

        return val

    @property
    def stdout(self) -> str:
        """
        Display the Chronospatial Computer's output.

        If a program outputs multiple values, they are separated by commas.
        """
        return ",".join(str(n) for n in self._stdout)

    def combo_operand(self, operand: int) -> int:
        """
        Convert the provided operand into its respective combo operand.

        Combo operands are mapped as follows:
            * Combo operands `0` through `3` represent literal values `0` through `3`
            * Combo operand `4` represents the value of register `A`
            * Combo operand `5` represents the value of register `B`
            * Combo operand `6` represents the value of register `C`
            * Combo operand `7` is reserved and will not appear in a valid program
        """
        if operand in {0, 1, 2, 3}:
            return operand

        if operand == 4:
            return self.registers["A"]
        if operand == 5:
            return self.registers["B"]
        if operand == 6:
            return self.registers["C"]

        raise ValueError(f"Unknown/reserved operand: '{operand}'")

    def run(self) -> None:
        """Execute the loaded program until halted."""
        opcode_mapping = {
            OpCode.ADV: self.adv,
            OpCode.BXL: self.bxl,
            OpCode.BST: self.bst,
            OpCode.JNZ: self.jnz,
            OpCode.BXC: self.bxc,
            OpCode.OUT: self.out,
            OpCode.BDV: self.bdv,
            OpCode.CDV: self.cdv,
        }

        while True:
            try:
                instruction = OpCode(self.read())
                operand = self.read()
            except HaltError:
                break

            opcode_mapping[instruction](operand)

    def _div(self, combo_operand: int, store: str) -> None:
        """
        Perform Chronospatial division & store the result in the specified register.

        The numerator is the value in the A register. The denominator is found by raising 2 to the
        power of the instruction's combo operand. The result of the division operation is truncated
        to an integer and then written to the specified register.
        """
        numerator = self.registers["A"]
        denominator = 2**combo_operand
        self.registers[store] = int(numerator / denominator)

    def adv(self, operand: int) -> None:
        """
        Perform Chronospatial division & store the result in the specified register.

        The numerator is the value in the A register. The denominator is found by raising 2 to the
        power of the instruction's combo operand. The result of the division operation is truncated
        to an integer and then written to the `A` register.
        """
        operand = self.combo_operand(operand)
        self._div(operand, "A")

    def bxl(self, operand: int) -> None:
        """Calc the bitwise XOR of register `B` and the literal operand, writing to register `B`."""
        self.registers["B"] = self.registers["B"] ^ operand

    def bst(self, operand: int) -> None:
        """Calc the combo operand `mod 8`, writing to register `B`."""
        operand = self.combo_operand(operand)
        self.registers["B"] = operand % 8

    def jnz(self, operand: int) -> None:
        """Jump the instruction pointer to the literal operand if register `A` is not `0`."""
        if self.registers["A"] == 0:
            return
        else:
            self._pointer = operand

    def bxc(self, operand: int) -> None:
        """
        Calc the bitwise XOR of register `B` and register `C`, writing to register `B`.

        NOTE: For legacy reasons, this instruction reads an operand but ignores it.
        """
        self.registers["B"] = self.registers["B"] ^ self.registers["C"]

    def out(self, operand: int) -> None:
        """
        Calc the combo operand `mod 8` and write to `stdout`.

        NOTE: If a program outputs multiple values, they are separated by commas.
        """
        operand = self.combo_operand(operand)
        self._stdout.append(operand % 8)

    def bdv(self, operand: int) -> None:
        """
        Perform Chronospatial division & store the result in the specified register.

        The numerator is the value in the A register. The denominator is found by raising 2 to the
        power of the instruction's combo operand. The result of the division operation is truncated
        to an integer and then written to the `B` register.
        """
        operand = self.combo_operand(operand)
        self._div(operand, "B")

    def cdv(self, operand: int) -> None:
        """
        Perform Chronospatial division & store the result in the specified register.

        The numerator is the value in the A register. The denominator is found by raising 2 to the
        power of the instruction's combo operand. The result of the division operation is truncated
        to an integer and then written to the `C` register.
        """
        operand = self.combo_operand(operand)
        self._div(operand, "C")

    @classmethod
    def from_debug(cls, dump: str) -> ChronoComp:
        """
        Restore a Chronocomputer's state from the provided debug information.

        The debug information is assumed to be of the following form:

        ```
        Register A: 729
        Register B: 0
        Register C: 0

        Program: 0,1,5,4,3,0
        ```
        """
        raw_registers, raw_program = dump.split("\n\n")

        split_registers = re.findall(r"Register (\w+): (\d+)", raw_registers)
        if len(split_registers) != 3:
            raise ValueError(
                f"Could not identify all registers. Found: {len(split_registers)}, expected: 3"
            )

        registers = {reg: int(v) for reg, v in split_registers}

        _, comps = raw_program.split(":")
        program = tuple(int(n) for n in comps.split(","))

        return cls(registers=registers, program=program)


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    ccomp = ChronoComp.from_debug(puzzle_input)
    ccomp.run()
    print(f"Part One: {ccomp.stdout}")

    print(f"Part Two: {...}")
