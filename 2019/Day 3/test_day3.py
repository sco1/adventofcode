import pytest
from aoc_2019_day3 import Wire


# Test cases as (wire a, wire b, truth Manhattan distance) tuples
PART_ONE = [
    ("R8,U5,L5,D3", "U7,R6,D4,L4", 6),
    ("R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83", 159),
    ("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7", 135),
]

# Test cases as (wire a, wire b, truth step distance) tuples
PART_TWO = [
    ("R8,U5,L5,D3", "U7,R6,D4,L4", 30),
    ("R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83", 610),
    ("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7", 410),
]


@pytest.mark.parametrize("diagram_a, diagram_b, truth_distance", PART_ONE)
def test_part_one(diagram_a: str, diagram_b: str, truth_distance: int) -> None:
    """Test for correct program output calculation."""
    wire_a = Wire(diagram_a)
    wire_b = Wire(diagram_b)
    closest_distance = wire_a.closest_intersect_manhattan(wire_b)[1]

    assert closest_distance == truth_distance


@pytest.mark.parametrize("diagram_a, diagram_b, truth_steps", PART_TWO)
def test_part_two(diagram_a: str, diagram_b: str, truth_steps: int) -> None:
    """Test for correct program output calculation."""
    wire_a = Wire(diagram_a)
    wire_b = Wire(diagram_b)

    closest_distance = wire_a.closest_intersect_steps(wire_b)[1]

    assert closest_distance == truth_steps
