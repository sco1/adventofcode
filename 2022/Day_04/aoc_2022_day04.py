from pathlib import Path


def parse_assignments(raw_assignments: list[str]) -> list[list[range]]:
    """
    Parse the provided assignment pairs into a list of `range` pairs.

    Paired section assignments are assumed to be provided in the form `2-4,6-8`, where sections can
    be any positive integer.
    """
    out_assignments = []
    for elf_group in raw_assignments:
        elves = elf_group.split(",")

        elf_ranges = []
        for elf in elves:
            lbound, rbound = elf.split("-")
            elf_ranges.append(range(int(lbound), int(rbound) + 1))

        out_assignments.append(elf_ranges)

    return out_assignments


def check_full_overlap(assignments: list[range]) -> bool:
    """Return `True` if one of the provided pairs of ranges is fully contained by the other."""
    if len(assignments) != 2:
        raise ValueError(f"Can only check pairs of ranges. Received {len(assignments)}.")

    lrange, rrange = assignments
    return (lrange[0] in rrange and lrange[-1] in rrange) or (
        rrange[0] in lrange and rrange[-1] in lrange
    )


def check_any_overlap(assignments: list[range]) -> bool:
    """Return `True` if one of the provided pairs of ranges is partially contained by the other."""
    if len(assignments) != 2:
        raise ValueError(f"Can only check pairs of ranges. Received {len(assignments)}.")

    lrange, rrange = assignments
    check_range = range(max(lrange.start, rrange.start), min(lrange.stop, rrange.stop))

    return bool(check_range)


def count_overlaps(raw_assignments: list[str]) -> tuple[int, int]:
    """Count the number of full and partial overlaps in the provided cleaning schedule."""
    full = sum(
        check_full_overlap(assignment_pair)
        for assignment_pair in parse_assignments(raw_assignments)
    )

    partial = sum(
        check_any_overlap(assignment_pair) for assignment_pair in parse_assignments(raw_assignments)
    )

    return full, partial


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().splitlines()

    full, partial = count_overlaps(puzzle_input)
    print(f"Part One: {full}")
    print(f"Part Two: {partial}")
