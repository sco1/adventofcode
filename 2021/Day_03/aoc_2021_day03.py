import typing as t
from collections import Counter
from pathlib import Path


def _transpose_report(diagnostic_report: list[str]) -> t.Generator[str, None, None]:
    """Transpose the provided report and yield its columns as strings."""
    for col in zip(*diagnostic_report):
        yield col


def _count_bits(diagnostic_report: list[str]) -> t.Generator[tuple[int, int], None, None]:
    """Count the number of zero and one bits in the provided diagnostic report."""
    for col in _transpose_report(diagnostic_report):
        yield col.count("0"), col.count("1")


def calculate_power_consumption(diagnostic_report: list[str]) -> int:
    """
    Calculate the submarine's power consumption using the provided diagnostic report.

    Power consumption is determined by multiplying together the gamma rate and the epsilon rate,
    which are generating using the most and least common bit, column-wise, from the given diagnostic
    report.

    It is assumed that all values in the provided report have the same number of columns.
    """
    gamma_rate = []
    epsilon_rate = []  # Could also just flip gamma's bits but this is simple enough
    for n_zeros, n_ones in _count_bits(diagnostic_report):
        if n_zeros > n_ones:
            gamma_rate.append("0")
            epsilon_rate.append("1")
        else:
            gamma_rate.append("1")
            epsilon_rate.append("0")

    gamma_rate = int("".join(gamma_rate), 2)
    epsilon_rate = int("".join(epsilon_rate), 2)

    return gamma_rate * epsilon_rate


def _common_bit(diagnostic_report: list[str], col_idx: int, is_most: bool) -> str:
    """
    Calculate the most or least common bit for each column of the provided report.

    In the event of a tie, the output will be the string equivalent of the `is_most` flag.
    """
    bit_count = Counter(row[col_idx] for row in diagnostic_report)
    high, low = bit_count.most_common()

    if high[1] == low[1]:
        # Break ties
        if is_most:
            return "1"
        else:
            return "0"
    elif is_most:
        return high[0]
    else:
        return low[0]


def _bit_criteria_select(report: list[str], is_most: bool) -> int:
    """
    Locate the query value from the diagnostic report based on the provided bit criteria.

    For the given report, report values are iterated over by bit position. For each position, the
    most/least common value in the current bit position is calculated, only numbers with that bit in
    that position are retained. In the event of a tie, 1 is used when calculating the most common
    and 0 is used when calculating the least common. This process is repeated until there is only
    one value from the report remaining.

    It is assumed that the provided diagnostic report contains at most one value that can be
    selected by the above criteria, and that all values in the report have the same number of
    columns.
    """
    n_cols = len(report[0])
    for col_idx in range(n_cols):
        select_bit = _common_bit(report, col_idx, is_most)
        report = [row for row in report if row[col_idx] == select_bit]

        if len(report) == 1:
            return int(report[0], 2)


def calculate_life_support_rating(diagnostic_report: list[str]) -> int:
    """
    Calculate the life support rating of the submarine based on the provided report.

    The life support rating is defined as the product of the Oxygen Generator Rating (OGR) and CO2
    Scrubber Rating (CSR). The OGR is selected using the most common bit in each column, and the CSR
    using the least common bit in each column.
    """
    return _bit_criteria_select(diagnostic_report, True) * _bit_criteria_select(
        diagnostic_report, False
    )


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().splitlines()

    print(f"Part One: {calculate_power_consumption(puzzle_input)}")
    print(f"Part Two: {calculate_life_support_rating(puzzle_input)}")
