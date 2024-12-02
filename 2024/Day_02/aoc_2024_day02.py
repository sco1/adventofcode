import itertools
from collections import abc
from pathlib import Path


def parse_level_report(raw_report: str) -> list[list[int]]:
    """
    Parse the raw Red-Nosed Reactor level report provided by The Historians.

    Level reports are assumed to be provided as rows of space-delimited integers, e.g.:

    ```
    7 6 4 2 1
    1 2 7 8 9
    ```
    """
    parsed_report = []
    for line in raw_report.splitlines():
        if not line:
            continue

        parsed_report.append([int(n) for n in line.split()])

    return parsed_report


def is_level_safe(levels: abc.Iterable[int]) -> bool:
    """
    Determine if the provided level report is safe.

    A report is deemed safe if the following critera are all met:
      * The levels are either all increasing or all decreasing
      * Any two adjacent levels differ by at least one and at most three
    """
    deltas = [(e - s) for s, e in itertools.pairwise(levels)]
    should_increase = deltas[0] > 0
    for d in deltas:
        if any(
            (
                (abs(d) > 3) or (d == 0),
                should_increase and (d < 0),
                not should_increase and (d > 0),
            )
        ):
            return False

    return True


def is_level_safe_with_dampener(levels: list[int]) -> bool:
    """
    Determine if the provided level report is safe if a Problem Dapener is mounted to the reactor.

    The problem dapener lets the reactor safety systems tolerate a single bad level in what would
    otherwise be a safe report.

    A report is deemed safe if the following critera are all met:
      * The levels are either all increasing or all decreasing
      * Any two adjacent levels differ by at least one and at most three
    """
    # Since the inputs are relatively short we can brute force this by dropping each value until
    # we either get a report that works or we run to the end and it's still unsafe
    for i in range(len(levels)):
        popped_report = levels[:i] + levels[i + 1 :]
        if is_level_safe(popped_report):
            return True

    return False


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    parsed_reports = parse_level_report(puzzle_input)

    print(f"Part One: {sum(is_level_safe(report) for report in parsed_reports)}")
    print(f"Part Two: {sum(is_level_safe_with_dampener(report) for report in parsed_reports)}")
