from __future__ import annotations

import itertools
import math
import typing as t
from collections import deque
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MachineInstruction:  # noqa: D101
    name: str
    op: t.Callable
    n_params: int
    writes: bool


class IntcodeMachine:
    """Intcode computer information goes here."""

    OPCODES: dict[int, MachineInstruction]
    PARAMETER_MODE: dict[int, t.Callable]

    MAX_CYCLES: int = 1_000

    stdin: deque[str]
    stdout: deque[str]

    _initial_state: tuple[int, ...]
    _state: list[int]
    _cur: int

    def __init__(self, program: str, stdin: str = "") -> None:
        self.OPCODES = {
            1: MachineInstruction(name="add", op=self.add, n_params=3, writes=True),
            2: MachineInstruction(name="mul", op=self.mul, n_params=3, writes=True),
            3: MachineInstruction(name="input", op=self.inp, n_params=1, writes=True),
            4: MachineInstruction(name="output", op=self.out, n_params=1, writes=False),
        }

        self.PARAMETER_MODE = {
            0: self.read,  # Position
            1: lambda x: x,  # Immediate (aka value)
        }

        self._initial_state = tuple(int(c) for c in program.split(","))
        self.reset()

        if stdin:
            self.stdin = deque([stdin])
        else:
            self.stdin = deque()

        self.stdout = deque()

    @property
    def output(self) -> int:
        """Return the machine's output, as stored at address 0 of the processed program."""
        return self._state[0]

    def reset(self) -> None:
        """Reset the machine's memory to its original state."""
        self._state = list(self._initial_state)
        self._cur = 0

    def _apply_noun_verb(self, noun: int | None, verb: int | None) -> None:
        """Replace values at addresses `1` (noun) & `2` (verb), if provided."""
        if noun is not None:
            self._state[1] = noun

        if verb is not None:
            self._state[2] = verb

    def read(self, idx: int | None = None) -> int:
        """
        Read the value from the specified index.

        If no index is provided, the instruction pointer is used.
        """
        if idx is None:
            idx = self._cur

        return self._state[idx]

    def step(self, n: int = 1) -> int:
        """Advance the pointer `n` places, optionally returning the value at the resulting index."""
        self._cur += n
        return self.read()

    def jump(self, idx: int) -> int:
        """Move the pointer to `idx`, optionally returning the value at the resulting index."""
        self._cur = idx
        return self.read()

    def _resolve_params(
        self, raw_params: list[int], modes: int, instruction: MachineInstruction
    ) -> list[int]:
        """
        Take raw parameter values & modes and resolve them based on their parameter modes.

        Parameter modes are stored in the same value as the instruction's opcode; the opcode is a
        two-digit number based only on the ones and tens digit of the value. Parameter modes are
        single digits, one per parameter, read right-to-left from the opcode: the first parameter's
        mode is in the hundreds digit, the second parameter's mode is in the thousands digit, etc.

        Any missing modes are `0` (position).
        """
        # Use an intermediate string to obtain any missing leading zeros, since we've already parsed
        # into an integer
        # Reverse because parameter modes go from right to left
        param_modes = [int(mode) for mode in reversed(str(modes).zfill(len(raw_params)))]
        params = [self.PARAMETER_MODE[mode](val) for val, mode in zip(raw_params, param_modes)]

        # Parameters that an instruction writes to will never be in immediate mode, so they'll be
        # accidentally converted to the looked up value. We want to change this back to the index.
        if instruction.writes:
            params[-1] = raw_params[-1]

        return params

    def run(self, noun: int | None = None, verb: int | None = None) -> None:
        """
        Excecute the loaded program until opcode `99` is reached, terminating the program.

        Prior to execution, the computer state is reset and, if provided, the noun/verb pair is
        applied.
        """
        self.reset()
        self._apply_noun_verb(noun, verb)

        cycle = 0
        while True:
            # Parameter modes are stored in the same value as the instruction's opcode; the opcode
            # is a two-digit number based only on the ones and tens digit of the value. Parameter
            # modes are single digits, one per parameter, read right-to-left from the opcode: the
            # first parameter's mode is in the hundreds digit, the second parameter's mode is in the
            # thousands digit, etc.. Any missing modes are 0.
            opc_chunk = self.read()
            opc = opc_chunk % 100
            if opc == 99:  # Terminate program
                return

            if cycle > self.MAX_CYCLES:
                raise Exception(f"Maximum cycles exceeded: {self.MAX_CYCLES}")

            instruction = self.OPCODES.get(opc, None)
            if instruction is None:
                raise Exception(f"Unknown opcode: {opc}")

            params = self._resolve_params(
                raw_params=[self.step() for _ in range(instruction.n_params)],
                modes=opc_chunk // 100,
                instruction=instruction,
            )
            instruction.op(params)

            self.step()
            cycle += 1

    def add(self, params: t.Iterable[int]) -> None:
        """
        Multiply the input parameter(s) and place the result at the specified index.

        It is assumed that at least 2 parameters are received. The final value specified the put
        index for the result, the rest of the parameters are assumed to specify the indices of the
        value(s) to sum.
        """
        *vals, put_idx = params
        self._state[put_idx] = sum(vals)

    def mul(self, params: t.Iterable[int]) -> None:
        """
        Multiply the input parameter(s) and place the result at the specified index.

        It is assumed that at least 2 parameters are received. The final value specified the put
        index for the result, the rest of the parameters are assumed to specify the indices of the
        value(s) to multiply.
        """
        *vals, put_idx = params
        self._state[put_idx] = math.prod(vals)

    def inp(self, put_idx: int) -> None:
        """Pop input from stdin and place it at the specified index."""
        self._state[put_idx] = int(self.stdin.pop())

    def out(self, idx: int) -> None:
        """Append input to stdout, newest -> oldest."""
        self.stdout.appendleft(str(self._state[idx]))


def find_noun_verb(program: str, target_output: int, max_val: int = 99) -> tuple[int, int]:
    """Given the starting program, iterate over noun/verb pairs until target output is received."""
    im = IntcodeMachine(program)
    for noun, verb in itertools.product(range(max_val + 1), repeat=2):
        # Assuming that the first instruction uses the values in locations 1 and 2 as indices, we
        # can skip these noun/verb values since they'll reference unreachable locations
        if noun >= len(im._state) or verb >= len(im._state):
            continue

        im.run(noun, verb)
        if im.output == target_output:
            return (noun, verb)

    raise ValueError("No noun/verb pair found that produces the output target.")
