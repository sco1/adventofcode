import pytest

from .aoc_2018_day5 import improve_polymer, react_polymer

PART_ONE_CASES = (
    ("aA", 0),
    ("abBA", 0),
    ("abAB", 4),
    ("aabAAB", 6),
    ("dabAcCaCBAcCcaDA", 10),
)


@pytest.mark.parametrize(("polymer", "truth_units"), PART_ONE_CASES)
def test_part_one(polymer: str, truth_units: int) -> None:
    assert react_polymer(polymer) == truth_units


PART_TWO_CASES = (("dabAcCaCBAcCcaDA", 4),)


@pytest.mark.parametrize(("polymer", "truth_units"), PART_TWO_CASES)
def test_part_two(polymer: str, truth_units: int) -> None:
    assert improve_polymer(polymer) == truth_units
