from textwrap import dedent

import pytest
from aoc_2015_day7 import CircuitDiagram


PART_ONE = {
    "input": dedent(
        """\
        123 -> x
        456 -> y
        x AND y -> d
        x OR y -> e
        x LSHIFT 2 -> f
        y RSHIFT 2 -> g
        NOT x -> h
        NOT y -> i
        """
    ),
    "output": [
        ("d", 72),
        ("e", 507),
        ("f", 492),
        ("g", 114),
        ("h", 65412),
        ("i", 65079),
        ("x", 123),
        ("y", 456),
    ],
}

WIRING_DIAGRAM = CircuitDiagram.from_puzzle_input(PART_ONE["input"])


@pytest.mark.parametrize("out_wire,expected_output", PART_ONE["output"])
def test_part_one(out_wire: str, expected_output: int) -> None:
    """Check against problem examples for correct wire outputs."""
    assert WIRING_DIAGRAM.solve_for(out_wire) == expected_output
