import pytest

from .aoc_2020_day15 import NumberGame

GAME_TEST_CASES = [
    ("0,3,6", 436, 175594),
    ("1,3,2", 1, 2578),
    ("2,1,3", 10, 3544142),
    ("1,2,3", 27, 261214),
    ("2,3,1", 78, 6895259),
    ("3,2,1", 438, 18),
    ("3,1,2", 1836, 362),
]


@pytest.mark.parametrize(("starting_nums", "check_val_2020", "check_val_30m"), GAME_TEST_CASES)
def test_numbers_game(starting_nums: str, check_val_2020: int, check_val_30m: int) -> None:
    """Check the game, instantiated with the provided starters, after 2020 and 30 million steps."""
    game_2020 = NumberGame(starting_nums)
    game_2020.step_n(2020)
    assert game_2020.last_seen == check_val_2020

    game_30m = NumberGame(starting_nums)
    game_30m.step_n(30_000_000)
    assert game_30m.last_seen == check_val_30m
