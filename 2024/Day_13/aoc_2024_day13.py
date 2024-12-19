from __future__ import annotations

import re
from collections import abc
from dataclasses import dataclass
from pathlib import Path

BUTTON_RE = re.compile(r"Button \w: X\+(\d+), Y\+(\d+)")
PRIZE_RE = re.compile(r"Prize: X=(\d+), Y=(\d+)")


@dataclass(slots=True)
class Button:  # noqa: D101
    x: int
    y: int

    @classmethod
    def from_raw(cls, raw: str) -> Button:
        """
        Parse the provided raw button specification into a `Button` instance.

        Button specifications are assumed to be provided as a string of the following form:

        ```
        Button a: X+b, Y+c
        ```

        Where `a` is the name of the button, and `b` and `c` specify the distance, as positive
        integers, moved by the claw for each button press along the X-axis and Y-axis, respectively.
        Note that the button name is currently not preserved.
        """
        comps = BUTTON_RE.findall(raw)
        if not comps:
            raise ValueError(f"Could not identify button components from string: '{raw}'")

        return cls(x=int(comps[0][0]), y=int(comps[0][1]))


@dataclass(slots=True)
class Prize:  # noqa: D101
    x: int
    y: int

    @classmethod
    def from_raw(cls, raw: str) -> Prize:
        """
        Parse the provided raw prize location into a `Prize` instance.

        Prize locations are assumed to be provided as a string of the following form:

        ```
        Prize: X=a, Y=b
        ```

        Where `a` and `b` specify the location, as positive integers, of the prize inside the claw
        machine.
        """
        comps = PRIZE_RE.findall(raw)
        if not comps:
            raise ValueError(f"Could not identify prize components from string: '{raw}'")

        return cls(x=int(comps[0][0]), y=int(comps[0][1]))


@dataclass(slots=True)
class ClawMachine:  # noqa: D101
    a: Button
    b: Button
    prize: Prize

    def calculate_prize_presses(self) -> tuple[int, int] | None:
        """
        Calculate the minimum number of button presses required to reach the prize location.

        If the prize is not reachable using the stated button configuration, `None` is returned
        instead.
        """
        # We can approach this as the solution to a system of two linear equations:
        #    Ax_a + Bx_b = x_p
        #    Ay_a + By_b = y_p
        #
        # Where A & B are the number of presses of the A & B buttons, respectively
        #
        # We can then solve these by substitution, i.e. solve both equations for A, set them equal
        # to each other, then solve for B:
        #    A = (x_p - B*x_b) / x_a
        #    B = (x_a * y_p - x_p * y_a) / (x_a * y_b - x_b * y_a)
        #
        # Since we are working with integers only, not all equations will be solvable
        b_press = (self.a.x * self.prize.y - self.prize.x * self.a.y) / (
            self.a.x * self.b.y - self.b.x * self.a.y
        )
        if b_press != int(b_press):
            return None

        a_press = (self.prize.x - b_press * self.b.x) / self.a.x
        if a_press != int(a_press):
            return None

        return (int(a_press), int(b_press))

    def winning_token_cost(self) -> int | None:
        """
        Calculate the lowest token price required to win the claw machine prize.

        The total token price is calculated as: `3*n_A_presses + n_B_presses`. If the machine's
        prize is not obtainable, this function instead returns `None`.
        """
        presses = self.calculate_prize_presses()
        if presses is None:
            return None

        a_press, b_press = presses
        return 3 * a_press + b_press

    def add_prize_offset(self, offset: int) -> None:
        """Add the specified offset to the X and Y coordinates of the machine's prize."""
        self.prize.x += offset
        self.prize.y += offset

    @classmethod
    def from_raw(cls, raw: str) -> ClawMachine:
        """
        Parse the provided claw machine specification into a `ClawMachine` instance.

        Claw machine specifications are assumed to be provided as a string of the following form:

        ```
        Button A: X+94, Y+34
        Button B: X+22, Y+67
        Prize: X=8400, Y=5400
        ```

        See the documentation of the `from_raw` classmethods of the `Button` and `Prize` classes for
        additional details on the expected specification form.
        """
        components = raw.splitlines()
        if len(components) != 3:
            raise ValueError(f"Too many lines: expected 3, received {len(components)}")

        raw_a, raw_b, raw_prize = components
        return cls(
            a=Button.from_raw(raw_a),
            b=Button.from_raw(raw_b),
            prize=Prize.from_raw(raw_prize),
        )


def parse_machine_spec(raw_specs: str, prize_offset: int = 0) -> list[ClawMachine]:
    """
    Parse the provided machine specifications into their equivalent `ClawMachine` instances.

    Machine specifications are assumed to be provided as a set of 3 newline delimited strings;
    multiple machines may be delimited by a blank line.

    For example:

    ```
    Button A: X+94, Y+34
    Button B: X+22, Y+67
    Prize: X=8400, Y=5400

    Button A: X+26, Y+66
    Button B: X+67, Y+21
    Prize: X=12748, Y=12176
    ```

    See the documentation of the `from_raw` classmethods of the `Button`, `Prize`, and `ClawMachine`
    classes for additional details on the expected specification form.

    A `prize_offset` may be optionally specified to be added to the X and Y components of each
    machine's prize location.
    """
    machines = [ClawMachine.from_raw(spec) for spec in raw_specs.split("\n\n")]
    for m in machines:
        m.add_prize_offset(prize_offset)

    return machines


def calculate_total_winning_cost(claw_machines: abc.Iterable[ClawMachine]) -> int:
    """Calculate the total token cost to obtain the prize across all winnable machines."""
    total_cost = 0
    for cm in claw_machines:
        cost = cm.winning_token_cost()
        if cost is not None:
            total_cost += cost

    return total_cost


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    machines = parse_machine_spec(puzzle_input)
    print(f"Part One: {calculate_total_winning_cost(machines)}")

    offset_machines = parse_machine_spec(puzzle_input, prize_offset=10_000_000_000_000)
    print(f"Part Two: {calculate_total_winning_cost(offset_machines)}")
