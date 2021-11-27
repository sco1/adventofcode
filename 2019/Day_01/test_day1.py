import pytest
from aoc_2019_day1 import calculate_propellant, calculate_stage_propellant

# Test cases as (stage mass, fuel required) tuples
PART_ONE = [(12, 2), (14, 2), (1969, 654), (100756, 33583)]
PART_TWO = [(14, 2), (1969, 966), (100756, 50346)]


@pytest.mark.parametrize("stage_mass, truth_fuel", PART_ONE)
def test_part_one(stage_mass: int, truth_fuel: int) -> None:
    """Validate fuel requirement for the provided stage mass."""
    assert calculate_propellant(stage_mass) == truth_fuel


@pytest.mark.parametrize("stage_mass, truth_fuel", PART_TWO)
def test_part_two(stage_mass: int, truth_fuel: int) -> None:
    """Validate fuel requirement for the provided stage mass, accounting for fuel weight."""
    assert calculate_stage_propellant(stage_mass) == truth_fuel
