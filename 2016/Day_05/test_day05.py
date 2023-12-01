from .aoc_2016_day05 import calculate_door_password, calculate_door_password_positional


def test_password_gen() -> None:
    assert calculate_door_password("abc") == "18f47a30"


def test_positional_password_gen() -> None:
    assert calculate_door_password_positional("abc") == "05ace8e3"
