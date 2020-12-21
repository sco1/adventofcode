from textwrap import dedent

from .aoc_2020_day16 import calculate_error_rate, find_field_order, parse_puzzle_input


SAMPLE_INPUT_P1 = dedent(
    """\
    class: 1-3 or 5-7
    row: 6-11 or 33-44
    seat: 13-40 or 45-50

    your ticket:
    7,1,14

    nearby tickets:
    7,3,47
    40,4,50
    55,2,20
    38,6,12
    """
)


def test_part_one() -> None:  # noqa: D103
    assert calculate_error_rate(SAMPLE_INPUT_P1) == 71


SAMPLE_INPUT_P2 = dedent(
    """\
    class: 0-1 or 4-19
    row: 0-5 or 8-19
    seat: 0-13 or 16-19

    your ticket:
    11,12,13

    nearby tickets:
    3,9,18
    15,1,5
    5,14,9
    """
)


def test_part_two() -> None:  # noqa: D103
    validators, _, nearby_tickets = parse_puzzle_input(SAMPLE_INPUT_P2)
    field_order = find_field_order(validators, nearby_tickets)

    assert tuple(field_order.values()) == (1, 0, 2)
