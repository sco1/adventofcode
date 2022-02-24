import collections
import operator
import re
from pathlib import Path

OPS = {
    "<": operator.lt,
    "<=": operator.le,
    ">": operator.gt,
    ">=": operator.ge,
    "==": operator.eq,
    "!=": operator.ne,
}


INSTRUCTION_RE = re.compile(r"(\w+) (inc|dec) (-?\d+) if (\w+) ([<>=]+) (-?\d+)")


def execute(instructions: list[str]) -> tuple[int, int]:
    """
    Execute the provided register instructions & calculate the largest register values.

    Maximum register values are calulated both after the completion of the provided instructions &
    as the maximum register value encountered at any point during execution.

    Register instructions are assumed to be of the following form:
        * `<register> <"inc"/"dec"> <int> if <register> <conditional> <int>`

    ALl registers are initialized at `0`.
    """
    registers: dict[str, int] = collections.defaultdict(int)
    programmaticmax = 0
    for line in instructions:
        (
            target_register,
            modifier,
            increment,
            check_register,
            conditional,
            condition_val,
        ) = INSTRUCTION_RE.findall(line)[0]

        increment = int(increment)
        condition_val = int(condition_val)

        if modifier == "inc":
            if OPS[conditional](registers[check_register], condition_val):
                registers[target_register] += increment
        elif modifier == "dec":
            if OPS[conditional](registers[check_register], condition_val):
                registers[target_register] -= increment

        maxval = max(registers.values())
        if maxval > programmaticmax:
            programmaticmax = maxval

    return maxval, programmaticmax


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().splitlines()

    max_val, programmatic_max = execute(puzzle_input)

    print(f"Part One: {max_val}")
    print(f"Part Two: {programmatic_max}")
