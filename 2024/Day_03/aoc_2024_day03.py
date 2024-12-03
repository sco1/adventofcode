import math
import re
from pathlib import Path

MUL_RE = re.compile(r"mul\((\d+),(\d+)\)")
DO_DONT_BLOCK_RE = re.compile(r"don't\(\).*?(?:do\(\)|$)")


def find_operands(instruction: str) -> list[list[int]] | None:
    """
    Extract the operands from all valid `mul` operations in the provided instruction string.

    Valid `mul` operations are assumed to be of the form `mul(X,Y)`, where `X` and `Y` are each
    1-3 digit integers. Due to memory corruption, additional characters may be present in the
    instructions, invalidating the `mul` operation.

    For example:
        * `mul(4*` - Invalid
        * `mul(6,9!` - Invalid
        * `?(12,34)` - Invalid
        * `mul ( 2 , 4 )` - Invalid
        * `mul(44,46)` - Valid
        * `mul(123,4)` - Valid

    `mul` operations may also be nested. `xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)`, for example,
    contains two valid operations: `mul(2,4)` and `mul(5,5)`.

    Operands for each valid `mul` operation are parsed and returned by this function; if no valid
    `mul` operation is found, then `None` is returned.
    """
    mul_search = MUL_RE.findall(instruction)
    if mul_search:
        operands = [[int(n) for n in g] for g in mul_search]
        return operands
    else:
        return None


def calculate_instruction_result(instruction: str, do_dont: bool = False) -> int:
    """
    Calculate the sum of the products of all valid `mul` operations in the provided instruction.

    Due to memory corruption, additional characters may be present in the instructions,
    invalidating the `mul` operation. See the documentation for `find_operands` for specifics.

    If `do_dont` is `True`, the `do()` and `don't()` conditional statements are respected in the
    given instruction. `mul` operations following a `don't()` statement are disabled until either
    a `do()` statement is found or end end of the instruction is reached. `mul` operations are
    enabled at the beginning of the instruction.

    For example:

    ```
    xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
    ```

    Contains two active `mul` operations, `mul(2,4)` and `mul(8,5)`.

    If no valid `mul` operations are found, a no-op result of `0` is returned.
    """
    if do_dont:
        instruction = DO_DONT_BLOCK_RE.sub("", instruction)

    operands = find_operands(instruction)
    if operands:
        result = sum(math.prod(op) for op in operands)
        return result
    else:
        return 0  # Should be sufficient as a no-op instead of None?


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")

    # The newlines are a misdirection! Just junk data.
    puzzle_input = puzzle_input_file.read_text().replace("\n", " ")

    print(f"Part One: {calculate_instruction_result(puzzle_input)}")
    print(f"Part Two: {calculate_instruction_result(puzzle_input, do_dont=True)}")
