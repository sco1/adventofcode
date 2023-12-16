from collections import deque
from pathlib import Path


def score_groups(stream: str) -> tuple[int, int]:
    """
    Calculate the total score for all groups in the provided stream.

    A group is defined as a sequence that begins with `{` and ends with `}`. Within a group can be
    zero or more things, separated by commas. Since groups can contain other groups, a `}` only
    closes the most recently opened unclosed group.

    Within a group can be garbage, which is a sequence that begins with `<` and ends with `>` and
    can contain any character. Besides `>`, all characters within the garbage sequence have no
    special meaning (e.g. `{}` do not open/close a group). One exception is the `!` character, which
    means that the following character should be ignored.

    It is assumed that all groups and garbage sequences are properly terminated.

    The total score is calculated by summing each group's score; the group is assigned a score based
    on its depth. The outermost group gets a score of 1.
    """
    buffer = deque(stream)
    total_score = 0
    depth = 0
    in_garbage = False
    n_garbage = 0
    while buffer:
        c = buffer.popleft()

        if in_garbage:
            if c == "!":
                buffer.popleft()
                continue
            elif c == ">":
                in_garbage = False
                continue

            n_garbage += 1
            continue

        if c == "<":
            in_garbage = True
            continue

        if c == "{":
            depth += 1
        elif c == "}":
            total_score += depth
            depth -= 1

    return total_score, n_garbage


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    print(f"Part One: {score_groups(puzzle_input)[0]}")
    print(f"Part Two: {score_groups(puzzle_input)[1]}")
