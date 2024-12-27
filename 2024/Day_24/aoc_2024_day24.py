import re
import typing as t
from collections import abc, deque
from pathlib import Path

WIRING_RE = re.compile(r"(\w+) (\w+) (\w+) -> (\w+)")


class Wiring(t.NamedTuple):  # noqa: D101
    left: str
    right: str
    op: abc.Callable[[int, int], int]
    target: str

    def __str__(self) -> str:
        op_name = self.op.__name__.split("_")[1].upper()
        return f"{self.left} {op_name} {self.right} -> {self.target}"


def wire_and(left: int, right: int) -> int:  # noqa: D103
    return int(left and right)


def wire_or(left: int, right: int) -> int:  # noqa: D103
    return int(left or right)


def wire_xor(left: int, right: int) -> int:  # noqa: D103
    return int(left != right)


def parse_schematic(raw_schematic: str) -> tuple[dict[str, int], list[Wiring]]:
    """
    Parse the provided wiring schematic into its components.

    The wiring schematic is assumed to contain initial wire values along with the wiring schematic,
    delimited by a blank line, e.g.:

    ```
    x00: 1
    x01: 1

    x00 AND y00 -> z00
    x01 XOR y01 -> z01
    ```

    Note that the initial wiring values are not necessarily comprehensive; the wiring schematic only
    contains the initial values required for the circuit to complete.

    The wiring schematic describes how the gates are wired; all gates accept two boolean inputs and
    output a boolean to the target wire.
    """
    raw_initial, raw_wiring = raw_schematic.split("\n\n")

    initial_values: dict[str, int] = {}
    for line in raw_initial.splitlines():
        gate, raw_v = line.split(":")
        initial_values[gate] = int(raw_v)

    wires = []
    wiring = WIRING_RE.findall(raw_wiring)
    for w in wiring:
        left, raw_op, right, target = w

        if raw_op == "AND":
            op = wire_and
        elif raw_op == "OR":
            op = wire_or
        elif raw_op == "XOR":
            op = wire_xor
        else:
            raise ValueError(f"Unknown gate type: '{raw_op}'")

        wires.append(Wiring(left=left, right=right, op=op, target=target))

    return initial_values, wires


def run_circuit(wire_state: dict[str, int], wiring_diagram: list[Wiring]) -> int:
    """
    Execute the circuit schematic using the provided initial values.

    The circuit ultimately produces a number by comgining the bits on all wires that begin with `z`;
    `z00` is the least significant bit, then `z01`, then `z02`, and so on. For example, an end state
    of `{z00: 0, z01: 0, z:02: 1}` produces the binary number `100`, which is the decimal number
    `4`.
    """
    # Some wires may not have values yet, so we should be able to skip them until they're available
    wire_queue = deque(wiring_diagram)
    while wire_queue:
        w = wire_queue.popleft()

        try:
            wire_state[w.target] = w.op(wire_state[w.left], wire_state[w.right])
        except KeyError:
            wire_queue.append(w)

    z_bits = sorted(((k, v) for k, v in wire_state.items() if k.startswith("z")), reverse=True)
    raw_z = "".join(str(b[1]) for b in z_bits)
    return int(raw_z, 2)


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    print(f"Part One: {run_circuit(*parse_schematic(puzzle_input))}")
    print(f"Part Two: {...}")
