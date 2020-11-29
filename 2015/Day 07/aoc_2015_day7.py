from __future__ import annotations

import operator
import typing as t
from pathlib import Path


# Per the problem statement, we're working with 16-bit signals (0 to 65535) so some operators will
# need to be corrected to keep in that range (and, for NOT, not a bool)
OPS = {
    "INPUT": lambda l, _: l,
    "NOT": lambda _, r: ~r & 0xFFFF,
    "AND": operator.and_,
    "OR": operator.or_,
    "LSHIFT": lambda l, r: (l << r) & 0xFFFF,
    "RSHIFT": lambda l, r: (l >> r) & 0xFFFF,
}


class WireInstruction:
    """
    Represent a wiring instruction for little Bobby Tables' circuit diagram.

    The following instructions are supported:
        * INPUT: "l -> wire"
        * NOT: "NOR r -> wire"
        * AND: "l AND r -> wire"
        * OR: "l OR r -> wire"
        * LSHIFT: "l LSHIFT r -> wire"
        * RSHIFT: "l RSHIFT r -> wire"

    Where l and r can either be an integer constant or reference to another wire.
    """

    def __init__(
        self, lval: t.Union[str, int], op_name: str, rval: t.Union[str, int], out_wire: str
    ):
        self.lval = lval
        self.op_name = op_name
        self.op = OPS[op_name]
        self.rval = rval
        self.out_wire = out_wire

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.lval!r}, {self.op_name!r}, {self.rval!r}, {self.out_wire!r}"
            ")"
        )

    def __call__(self, diagram: dict[str, WireInstruction], results_cache: dict[str, int]):
        """Recursively solve the circuit diagram until we get the signal to our output wire."""
        # Per the problem description, output wires are only calculated once so when we see it the
        # calculations are done!
        if self.out_wire in results_cache:
            return results_cache[self.out_wire]

        # Otherwise, continue evaluating the current expression
        # Recursively resolve any references that are wires (str) rather than signals (int)
        lval, rval = (
            diagram[signal](diagram, results_cache) if isinstance(signal, str) else signal
            for signal in (self.lval, self.rval)
        )
        results_cache[self.out_wire] = self.op(lval, rval)

        return results_cache[self.out_wire]


class CircuitDiagram:
    """Represent Bobby Tables' holiday circuit diagram."""

    def __init__(self, wire_instructions: dict[str, WireInstruction]):
        self.wire_instructions = wire_instructions

    def solve_for(self, target_wire: str = "a") -> int:
        """Solve the circuit diagram for the output signal of the targeted wire."""
        return self.wire_instructions[target_wire](self.wire_instructions, {})

    @classmethod
    def from_puzzle_input(cls, puzzle_input: str) -> dict[str, WireInstruction]:
        """
        Parse the provided raw puzzle input into a circuit diagram.

        The following wiring instructions are supported:
            * INPUT: "l -> wire"
            * NOT: "NOR r -> wire"
            * AND: "l AND r -> wire"
            * OR: "l OR r -> wire"
            * LSHIFT: "l LSHIFT r -> wire"
            * RSHIFT: "l RSHIFT r -> wire"

        Where l and r can either be an integer constant or reference to another wire.

        Each wire can only get a signal from one source, but can provide its signal to multiple
        destinations.
        """
        input_lines = puzzle_input.splitlines()

        circuit_diagram = {}
        for line in input_lines:
            inputs, out_wire = line.split(" -> ")

            split_inputs = inputs.split()
            if len(split_inputs) == 1:
                # Input signal
                lval = cls._maybe_convert_input(split_inputs[0])
                op = "INPUT"
                rval = None
            elif len(split_inputs) == 2:
                # NOT gate
                lval = None
                op = split_inputs[0]
                rval = cls._maybe_convert_input(split_inputs[1])
            elif len(split_inputs) == 3:
                # Every other gate
                lval = cls._maybe_convert_input(split_inputs[0])
                op = split_inputs[1]
                rval = cls._maybe_convert_input(split_inputs[2])
            else:
                raise ValueError(f"Unknown Expression: '{line}'")

            circuit_diagram[out_wire] = WireInstruction(lval, op, rval, out_wire)

        return cls(circuit_diagram)

    @staticmethod
    def _maybe_convert_input(input_value: str) -> t.Union[str, int]:
        """Convert the input string to integer if it's digits, otherwise pass the string through."""
        if input_value.isdigit():
            return int(input_value)
        else:
            return input_value


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text()

    wiring_diagram = CircuitDiagram.from_puzzle_input(puzzle_input)
    part_1_result = wiring_diagram.solve_for("a")
    print(f"Part 1: a = {part_1_result}")

    wiring_diagram.wire_instructions["b"] = WireInstruction(part_1_result, "INPUT", None, "b")
    print(f"Part 2: a = {wiring_diagram.solve_for('a')}")
