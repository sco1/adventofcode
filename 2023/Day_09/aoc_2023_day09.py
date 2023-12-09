import itertools
from collections import deque
from pathlib import Path


def extrapolate(history: str, rewind: bool = False) -> int:
    """
    Identify the pattern in the provided history of sensor readings & extrapolate the next value.

    If `rewind` is true, a historical reading is extrapolated instead.
    """
    rows = [deque(int(v) for v in history.split())]
    while True:
        # Per the problem statement, eventually we'll get to a point where the derivative is 0
        if all((v == 0) for v in rows[-1]):
            break
        rows.append(deque((right - left) for left, right in itertools.pairwise(rows[-1])))

    # Once we're there, we can sum back up the pyramid and find the next value of the original list
    for lr, ur in itertools.pairwise(rows[::-1]):
        if rewind:
            ur.appendleft(ur[0] - lr[0])
        else:
            ur.append(lr[-1] + ur[-1])

    if rewind:
        return rows[0][0]
    else:
        return rows[0][-1]


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    print(f"Part One: {sum(extrapolate(line) for line in puzzle_input.splitlines())}")
    print(f"Part Two: {sum(extrapolate(line, rewind=True) for line in puzzle_input.splitlines())}")
