import pytest

from .AoC2017_Day4 import _validate_password

PART_ONE_CASES = (
    ("aa bb cc dd ee", True),
    ("aa bb cc dd aa", False),
    ("aa bb cc dd aaa", True),
)


@pytest.mark.parametrize(("password", "truth_is_valid"), PART_ONE_CASES)
def test_part_one(password: str, truth_is_valid: bool) -> None:
    assert _validate_password(password) == truth_is_valid


PART_TWO_CASES = (
    ("abcde fghij", True),
    ("abcde xyz ecdab", False),
    ("a ab abc abd abf abj", True),
    ("iiii oiii ooii oooi oooo", True),
    ("oiii ioii iioi iiio", False),
)


@pytest.mark.parametrize(("password", "truth_is_valid"), PART_TWO_CASES)
def test_part_two(password: str, truth_is_valid: bool) -> None:
    assert _validate_password(password, check_anagram=True) == truth_is_valid
