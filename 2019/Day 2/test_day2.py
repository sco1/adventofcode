from typing import List

import pytest
from aoc_2019_day2 import IntcodeMachine


# Test cases as (program, expected output) tuples
# For Part 1's test cases in the problem description, noun and verb are not specified so the program
# is not altered prior to processing.
PART_ONE = [
    ([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
    ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
    ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
    ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]),
    ([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50], [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]),
]

# Test cases as (program, target output, noun, verb) tuples
PART_TWO = [
    ([1, 1, 1, 0, 99], 2, 0, 0),
    ([1, 1, 1, 3, 2, 3, 11, 0, 99, 30, 40, 50], 3500, 9, 10),
]


@pytest.mark.parametrize("in_program, out_program", PART_ONE)
def test_part_one(in_program: List[int], out_program: List[int]) -> None:
    """Test for correct program output calculation."""
    machine = IntcodeMachine(in_program)
    assert machine.output == out_program[0]


@pytest.mark.parametrize("in_program, target_output, truth_noun, truth_verb", PART_TWO)
def test_part_two(
    in_program: List[int], target_output: int, truth_noun: int, truth_verb: int
) -> None:
    """Test for correct program output, noun, and verb calculation."""
    machine = IntcodeMachine.find_noun_verb(in_program, target_output)
    assert machine.output == target_output
    assert machine.noun == truth_noun
    assert machine.verb == truth_verb
