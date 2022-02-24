from pathlib import Path


def follow_jumps(jumps: list[int]) -> int:
    """
    Execute the provided jump instructions and determine the number of jumps to exit.

    After each jump, the offset of the instruction increases by `1`.
    """
    pos = 0
    nsteps = 0
    while pos < len(jumps):
        currentpos = pos

        # Jump and increase the offset of the current instruction by 1
        pos += jumps[pos]
        jumps[currentpos] += 1

        nsteps += 1

    return nsteps


def follow_strange_jumps(jumps: list[int]) -> int:
    """
    Execute the provided jump instructions and determine the number of jumps to exit.

    If the jump offset is `3` or more, decrease the offset value by `1` rather than increase by `1`.
    """
    pos = 0
    nsteps = 0
    while pos < len(jumps):
        currentpos = pos

        # Jump and increase the offset of the current instruction using the strange criteria
        pos += jumps[pos]
        if jumps[currentpos] >= 3:
            jumps[currentpos] -= 1
        else:
            jumps[currentpos] += 1

        nsteps += 1

    return nsteps


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text()
    jumps = [int(line) for line in puzzle_input.split()]

    print(f"Part One: {follow_jumps(jumps.copy())}")
    print(f"Part Two: {follow_strange_jumps(jumps.copy())}")
