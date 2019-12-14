import pytest
from aoc_2019_day4 import is_valid_password

# Test cases as (password, is valid password) tuples
PART_ONE = [
    (111111, True),
    (223450, False),
    (123789, False),
]

PART_TWO = [
    (112233, True),
    (123444, False),
    (111122, True),
]


@pytest.mark.parametrize("password, is_valid", PART_ONE)
def test_part_one(password: int, is_valid: bool) -> None:
    """Test for correct classification of password as valid/not valid."""
    assert is_valid_password(password) == is_valid


@pytest.mark.parametrize("password, is_valid", PART_TWO)
def test_part_two(password: int, is_valid: bool) -> None:
    """Test for correct classification of password as valid/not valid."""
    assert is_valid_password(password, strict=True) == is_valid
