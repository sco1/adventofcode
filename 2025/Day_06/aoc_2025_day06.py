import itertools
import math
import typing as t
from collections import abc
from pathlib import Path

COLS_T: t.TypeAlias = list[list[int]]


def _parse_row2col(raw_rows: abc.Iterable[str]) -> COLS_T:
    rows = []
    for r in raw_rows:
        rows.append([int(n) for n in r.split()])

    # Transpose
    n_cols = len(rows[0])
    cols = []
    for i in range(n_cols):
        cols.append([r[i] for r in rows])

    return cols


def _parse_cephalopod(raw_rows: abc.Iterable[str]) -> COLS_T:
    # First group digits by column, then join into their respective raw numbers
    # Use zip_longest in case the input has been stripped of trailing newlines
    raw_cols = list(itertools.zip_longest(*raw_rows, fillvalue=" "))
    collapsed = ("".join(c) for c in raw_cols)

    # Iterate over the raw values and split into actual columns of integers
    # Though our operations for this puzzle are both associative so order doesn't end up mattering,
    # reverse the values so we meet the spirit of the question
    cols = []
    buff: list[int] = []
    for cell in collapsed:
        if not cell.strip():  # Fully empty column, this is the delimiter
            buff.reverse()
            cols.append(buff)
            buff = []
            continue

        buff.append(int(cell))
    else:  # No dangling buffer
        if buff:
            buff.reverse()
            cols.append(buff)

    cols.reverse()
    return cols


def parse_worksheet(worksheet: str, cephalopod: bool = False) -> tuple[COLS_T, list[abc.Callable]]:
    """
    Parse the provided math homework into its numeric & operator components.

    The worksheet is assumed to contain columns of math problems, where one or more lines of space
    delimited columns are followed by a single row of operators. For example:

    ```
    1   2 3
    14 15 16
    *  +  +
    ```

    While colums are separated by a single space, space within each column may be significant,
    depending on the interpretation.

    If `cephalopod` is `False`, whitespace within the column is not significant, and the above
    example becomes:

    ```
    [
        [1, 14],
        [2, 15],
        [3, 16],
    ]
    ,
    [*, +, +]
    ```

    If `cephalopod is True`, the worksheet is interpreted assuming cephalopod math, which is written
    right-to-left in columns; each number is given in its own column, with the most significant
    digit at the top and the least significatnt digit at the bottom. The above example becomes:

    ```
    [
        [6, 31],
        [25, 1],
        [4, 11],
    ]
    ,
    [+, +, *]
    ```
    """
    *raw_rows, raw_operators = worksheet.splitlines()

    if cephalopod:
        cols = _parse_cephalopod(raw_rows)
    else:
        cols = _parse_row2col(raw_rows)

    operators: list[abc.Callable] = []
    for o in raw_operators.split():
        if o == "*":
            operators.append(math.prod)
        elif o == "+":
            operators.append(sum)
        else:
            raise ValueError(f"Unknown operator: '{o}'")

    if cephalopod:
        operators.reverse()

    return cols, operators


def execute_worksheet(
    cols: abc.Iterable[abc.Iterable[int]], operators: abc.Iterable[abc.Callable]
) -> int:
    """
    Execute the provided worksheet instructions and return the result.

    `cols` and `operators` are assumed to be the same size, where `cols` is a collection of columns
    of integers and `operators` is a collection of callables to execute on their respective column.
    It is assumed that the callables contained by `operators` are able to operate on an iterable of
    integers.
    """
    total = 0
    for col, op in zip(cols, operators):
        total += op(col)

    return total


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    print(f"Part One: {execute_worksheet(*parse_worksheet(puzzle_input))}")
    print(f"Part Two: {execute_worksheet(*parse_worksheet(puzzle_input, cephalopod=True))}")
