from __future__ import annotations

from collections import deque
from typing import Callable, List, NamedTuple, Optional


class MachineInstruction(NamedTuple):
    """Represent an IntcodeMachine machine instruction."""

    name: str
    operation: Callable
    n_parameters: int
    writes: bool


class IntcodeMachine:
    """Represent our Intcode computer & its operations."""

    def __init__(self, intcode: List[int], stdin: Optional[str] = None):
        self.ops = {
            1: MachineInstruction("add", self.add, 3, True),
            2: MachineInstruction("mul", self.mul, 3, True),
            3: MachineInstruction("input", self.prog_input, 1, True),
            4: MachineInstruction("output", self.output, 1, False),
            5: MachineInstruction("jump_true", self.jump_true, 2, False),
            6: MachineInstruction("jump_false", self.jump_false, 2, False),
            7: MachineInstruction("lt", self.lt, 3, True),
            8: MachineInstruction("eq", self.eq, 3, True),
            99: None,
        }

        self.parameter_modes = {
            0: self.read,
            1: lambda x: x,
        }

        self.intcode = intcode
        self.stdin = deque([stdin])
        self.stdout = deque()

    def reset(self) -> None:
        """Reset the computer back to its initial state."""
        self.memory = self.intcode.copy()
        self.ip = 0
        self.stdout.clear()

    def read(self, idx: Optional[int] = None) -> int:
        """
        Read the value from the specified index.

        If no index is provided, the instruction pointer is used.
        """
        if not idx:
            idx = self.ip
            self.move_ip()

        return self.memory[idx]

    def write(self, val: int, idx: Optional[int] = None) -> None:
        """
        Write the provided value to the specified index.

        If no index is provided, the instruction pointer is used.
        """
        if not idx:
            idx = self.ip

        self.memory[idx] = val

    def move_ip(self, idx: Optional[int] = None) -> None:
        """
        Move the instruction pointer to the specified index.

        If no index is provided, the instruction pointer incremented by one.
        """
        if idx:
            self.ip = idx
        else:
            self.ip += 1

    def add(self, left: int, right: int, put_idx: int) -> None:
        """Sum the input values & place them at the specified index in the full opcode."""
        self.write(left + right, put_idx)

    def mul(self, left: int, right: int, put_idx: int) -> None:
        """Multiply the input values & place them at the specified index in the full opcode."""
        self.write(left * right, put_idx)

    def prog_input(self, put_idx: int) -> None:
        """Pop input from stdin and place it at the specified index in the full opcode."""
        self.write(int(self.stdin.pop()), put_idx)

    def output(self, out: Optional[int] = 0) -> int:
        """Append input to stdout, newest -> oldest."""
        self.stdout.appendleft(out)

    def jump_true(self, predicate: int, jump_idx: int) -> None:
        """If the predicate is truthy, set the instruction pointer to the jump index."""
        if predicate:
            self.move_ip(jump_idx)

    def jump_false(self, predicate: int, jump_idx: int) -> None:
        """If the predicate is falsey, set the instruction pointer to the jump index."""
        if not predicate:
            self.move_ip(jump_idx)

    def lt(self, left: int, right: int, put_idx: int) -> None:
        """If left is less than right, store 1 in the specified output index, otherwise 0."""
        if left < right:
            self.write(1, put_idx)
        else:
            self.write(0, put_idx)

    def eq(self, left: int, right: int, put_idx: int) -> None:
        """If left is equal to right, store 1 in the specified output index, otherwise 0."""
        if left == right:
            self.write(1, put_idx)
        else:
            self.write(0, put_idx)

    def compute_vals(
        self, vals: List[int], modes: int, instruction: MachineInstruction
    ) -> List[int]:
        """Take the raw values & modes and parse them based on their parameter modes."""
        # Use an intermediate string to obtain any missing leading zeros, since our opcode is
        # already an int
        # Reverse because parameter modes go from right to left
        modes = [int(mode) for mode in reversed(str(modes).zfill(len(vals)))]
        out_vals = [self.parameter_modes[mode](val) for val, mode in zip(vals, modes)]

        # Correct for write instructions always being in position mode
        if instruction.writes:
            out_vals[-1] = vals[-1]

        return out_vals

    def run(self, noun: Optional[int] = None, verb: Optional[int] = None) -> None:
        """
        Execute the provided intcode.

        If noun and verb are optionally specified, they are substituded appropriately before
        program execution
        """
        self.reset()
        self.noun = noun
        self.verb = verb
        if self.noun:
            self.memory[1] = self.noun
        if self.verb:
            self.memory[2] = self.verb

        # Run the computer!
        while True:
            opcode_chunk = self.read()
            opcode = opcode_chunk % 100
            op = self.ops[opcode]
            if op is None:
                break

            modes = opcode_chunk // 100
            vals = self.compute_vals([self.read() for _ in range(op.n_parameters)], modes, op)
            op.operation(*vals)
