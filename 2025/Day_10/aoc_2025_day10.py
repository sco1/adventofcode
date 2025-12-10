import itertools
import typing as t
from pathlib import Path


class MachineSpec(t.NamedTuple):
    """Factory Machine initialization specifications."""

    light_diagram: list[bool]
    wiring_schematic: list[list[int]]
    joltage_requirement: list[int]

    n_lights: int
    n_buttons: int
    n_joltage_banks: int

    @classmethod
    def from_raw(cls, raw_spec: str) -> t.Self:
        """
        Parse the machine's initialization parameters from its manual.

        Machine specifications are assumed to be provided in the following form:

        ```
        [<indicator light diagram>] (<button wiring schematic(s)>) {<joltage requirements>}
        ```

        * The indicator light diagram is provided as a single sequence of characters enclosed by
        square brackets (`[]`), where `.` indicates off and `#` indicates on, e.g. `[.##.]`
        * Button wiring schematics are provided as one or more groups of comma-delimited integers
        enclosed by parentheses (`()`), where each integer represents an indicator light index, e.g.
        `(3) (1,3) (2)`
        * Joltage requirements are provided as a single sequence of comma-delimited integers
        enclosed by curly braces (`{}`), where each integer represents a joltage back requirement,
        e.g. `{3,5,4,7}`
        """
        raw_lights, *raw_schematics, raw_joltage = raw_spec.split()

        lights = [True if c == "#" else False for c in raw_lights.strip("[]")]
        joltage = [int(c) for c in raw_joltage.strip("{}").split(",")]

        schematics = []
        for s in raw_schematics:
            schematics.append([int(c) for c in s.strip("()").split(",")])

        return cls(
            light_diagram=lights,
            wiring_schematic=schematics,
            joltage_requirement=joltage,
            n_lights=len(lights),
            n_buttons=len(schematics),
            n_joltage_banks=len(joltage),
        )


def best_button_press(machine: MachineSpec) -> int:
    """Determine the fewest number of button presses necessary to achieve correct initialization."""
    # Since each button press is a toggle, the minimal solution will only require at most one press
    # of any button, which allows us to greatly constrain a brute force approach
    # I'm sure there's probably a smarter solution, but this works well enough for the puzzle
    for n_press in range(1, machine.n_buttons + 1):
        for press_sequence in itertools.combinations(machine.wiring_schematic, n_press):
            # For each button pressed, add up the number of times each light is toggled; mod 2 then
            # maps this back to a boolean end state
            end_state = [
                bool(sum(i in p for p in press_sequence) % 2) for i in range(machine.n_lights)
            ]

            # Since we're iterating from smallest to largest number of button presses, we can
            # return as soon as the first solution is found
            if end_state == machine.light_diagram:
                return n_press

    raise ValueError("Could not identify a toggle sequence that matches the desired state.")


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    specs = [MachineSpec.from_raw(m) for m in puzzle_input.splitlines()]

    print(f"Part One: {sum(best_button_press(s) for s in specs)}")
    print(f"Part Two: {...}")
