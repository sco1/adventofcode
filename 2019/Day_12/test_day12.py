from textwrap import dedent

import pytest
from aoc_2019_day12 import Planet


# Provide test cases as (starting moon map, steps to simulate, truth energy)
PART_ONE = [
    (
        dedent(
            """\
            <x=-1, y=0, z=2>
            <x=2, y=-10, z=-7>
            <x=4, y=-8, z=8>
            <x=3, y=5, z=-1>
            """
        ),
        10,
        179,
    ),
    (
        dedent(
            """\
            <x=-8, y=-10, z=0>
            <x=5, y=5, z=10>
            <x=2, y=-7, z=3>
            <x=9, y=-8, z=-3>
            """
        ),
        100,
        1940,
    ),
]

# Provide test cases as (starting moon map, truth steps)
PART_TWO = [
    (
        dedent(
            """\
            <x=-1, y=0, z=2>
            <x=2, y=-10, z=-7>
            <x=4, y=-8, z=8>
            <x=3, y=5, z=-1>
            """
        ),
        2772,
    ),
    (
        dedent(
            """\
            <x=-8, y=-10, z=0>
            <x=5, y=5, z=10>
            <x=2, y=-7, z=3>
            <x=9, y=-8, z=-3>
            """
        ),
        4686774924,
    ),
]


@pytest.mark.parametrize("moon_map, n_steps, truth_energy", PART_ONE)
def test_part_one(moon_map: str, n_steps: int, truth_energy: int) -> None:
    """Test for correct energy output after the provided number of simulation steps."""
    jupiter = Planet.from_moon_map(moon_map.splitlines())
    jupiter.advance_sim(n_steps)

    assert jupiter.total_energy == truth_energy


@pytest.mark.parametrize("moon_map, truth_steps", PART_TWO)
def test_part_two(moon_map: str, truth_steps: int) -> None:
    """Test that the number of steps before a state repeat matches the truth value."""
    jupiter = Planet.from_moon_map(moon_map.splitlines())

    assert jupiter.find_repeat() == truth_steps
