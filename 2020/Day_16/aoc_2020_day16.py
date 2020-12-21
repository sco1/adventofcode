import math
import re
import typing as t
from collections import defaultdict
from pathlib import Path

import more_itertools as mit

VALIDATOR_RE = re.compile(r"([A-Za-z ]+): (\d+)-(\d+) or (\d+)-(\d+)")

VALIDATOR_T = dict[str, tuple[t.Sequence, t.Sequence]]
TICKET_T = list[int]


def parse_field_ranges(raw_validators: str) -> VALIDATOR_T:
    """
    Parse ticket field validators out of the raw specification string.

    Validators are assumed to be of the form:
        `"class: 1-3 or 5-7"`

    Where every field has two inclusive ranges of valid values.
    """
    validators = {}

    for validator in VALIDATOR_RE.findall(raw_validators):
        name, l_start, l_end, r_start, r_end = validator
        validators[name] = (
            range(int(l_start), int(l_end) + 1),
            range(int(r_start), int(r_end) + 1),
        )

    return validators


def parse_puzzle_input(raw_puzzle_input: str) -> tuple[VALIDATOR_T, TICKET_T, list[TICKET_T]]:
    """
    Split the raw puzzle input into its components.

    Puzzle input is assumed to contain only 3 chunks, delimited by a blank line:
        * Validators (e.g. `"class: 1-3 or 5-7"`)
        * My ticket (single line of CSV, with header)
        * Nearby tickets (multiple lines of CSV, with header)
    """
    raw_fields, raw_my_ticket, raw_nearby_tickets = raw_puzzle_input.split("\n\n")

    validators = parse_field_ranges(raw_fields)

    my_ticket = [int(n) for n in raw_my_ticket.split("\n")[1].split(",")]  # Skip header line

    nearby_tickets = []
    for ticket in raw_nearby_tickets.splitlines()[1:]:  # Skip header line
        nearby_tickets.append([int(n) for n in ticket.split(",")])

    return validators, my_ticket, nearby_tickets


def calculate_error_rate(raw_puzzle_input: str) -> int:
    """
    Calculate the sum of all invalid values contained in the nearby tickets.

    Values are considered invalid if they are not contained by any of the validation ranges.
    """
    validators, _, nearby_tickets = parse_puzzle_input(raw_puzzle_input)

    invalid_values = []
    for ticket in nearby_tickets:
        for val in ticket:
            if not any(val in check_range for check_range in mit.flatten(validators.values())):
                invalid_values.append(val)

    return sum(invalid_values)


def _check_column(col: int, ranges: tuple[t.Sequence, t.Sequence], tickets: list[TICKET_T]) -> bool:
    """Check that all values in the specified ticket column lie in at least one of the ranges."""
    l_check = [ticket[col] in ranges[0] for ticket in tickets]
    r_check = [ticket[col] in ranges[1] for ticket in tickets]

    return all(l | r for l, r in zip(l_check, r_check))  # noqa: E741


def find_field_order(validators: VALIDATOR_T, nearby_tickets: list[TICKET_T]) -> dict[str, int]:
    """
    Determine the order of fields on the train tickets.

    Field order is calculated only from valid nearby tickets
    """
    valid_tickets = []
    for ticket in nearby_tickets:
        for val in ticket:
            if not any(val in check_range for check_range in mit.flatten(validators.values())):
                break
        else:
            valid_tickets.append(ticket)

    # Iterate through columns & determine which are valid matches for each field
    field_candidates = defaultdict(set)
    n_columns = len(valid_tickets[0])
    for field_name, ranges in validators.items():
        for n in range(n_columns):
            if _check_column(n, ranges, valid_tickets):
                field_candidates[field_name].add(n)

    # Whittle down the candidates until we get a 1:1 mapping
    n_fields = len(validators)
    while sum(len(candidates) for candidates in field_candidates.values()) > n_fields:
        # A field has been found if its column subset only has one value
        found_columns = set.union(
            *(subset for subset in field_candidates.values() if len(subset) == 1)
        )

        # Iterate through columns with more than one possibility & remove any found columns
        for field_name, subset in field_candidates.items():
            if len(subset) > 1:
                field_candidates[field_name] = subset - found_columns

    # "de-set" final output so we don't have to transform later
    # Since there should only be one integer in each subset, we can just pop it out rather than
    # converting to something like a list/tuple and indexing
    field_mapping = {field_name: mapping.pop() for field_name, mapping in field_candidates.items()}

    return field_mapping


def calculate_departure_product(raw_puzzle_input: str) -> int:
    """Map field names to ticket columns & calculate the product of the `"departure"` fields."""
    validators, my_ticket, nearby_tickets = parse_puzzle_input(raw_puzzle_input)
    field_order = find_field_order(validators, nearby_tickets)

    return math.prod(
        my_ticket[idx]
        for field_name, idx in field_order.items()
        if field_name.startswith("departure")
    )


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text()

    print(f"Part One: {calculate_error_rate(puzzle_input)}")
    print(f"Part Two: {calculate_departure_product(puzzle_input)}")
