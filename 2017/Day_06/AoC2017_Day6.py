from pathlib import Path


def _findmax(banks: list[int]) -> tuple[int, int]:
    """Find the maximum value and its first location in the provided list."""
    max_blocks = max(banks)
    max_idx = banks.index(max_blocks)

    return max_blocks, max_idx


def reallocate_banks(banks: list[int]) -> tuple[int, int]:
    """
    Perform the memory reallocation routine & determine how many cycles before a loop is reached.

    For each step in the reallocation cycle, the memory bank with the most blocks is found (ties are
    won by the lowest-numbered memory bank), and its blocks are redistributed across all the banks.
    Distribution is accomplished by moving to the next block (by index) and inserting a block,
    continuing until blocks are exhausted and wrapping around if necessary.

    Once a loop is detected, the total number of steps is provided along with the number of cycles
    from when the repeated memory state was first encountered to loop detection.
    """
    # Track the cycle count when a bank configuration is seen so we can calculate loop size
    seen = {tuple(banks): 0}
    n_steps = 0
    while True:
        # Find the memory bank with the most blocks & redistribute its blocks across all the banks,
        # wrapping around if necessary (the bank can possibly get some back)
        n_blocks, max_idx = _findmax(banks)
        banks[max_idx] = 0
        idxlist = (x % len(banks) for x in range(max_idx + 1, max_idx + n_blocks + 1))
        for idx in idxlist:
            banks[idx] += 1

        n_steps += 1
        next_bank = tuple(banks)
        if next_bank in seen:
            return n_steps, n_steps - seen[next_bank]
        else:
            seen[next_bank] = n_steps


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()
    banks = [int(line) for line in puzzle_input.split()]

    n_steps, loop_size = reallocate_banks(banks)
    print(f"Part One: {n_steps}")
    print(f"Part Two: {loop_size}")
