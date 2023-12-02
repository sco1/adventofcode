from textwrap import dedent

import pytest

from .aoc_2023_day02 import Game, find_valid_games

VALID_GAME_TEST_CASES = (
    ("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green", True),
    ("Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue", True),
    ("Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red", False),
    ("Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red", False),
    ("Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green", True),
)


@pytest.mark.parametrize(("game_spec", "truth_is_valid"), VALID_GAME_TEST_CASES)
def test_valid_game(game_spec: str, truth_is_valid: bool) -> None:
    g = Game(game_spec)
    assert g.is_possible(red=12, green=13, blue=14) is truth_is_valid


SAMPLE_INPUT = dedent(
    """\
    Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
    Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
    Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
    Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
    """
)


def test_valid_games() -> None:
    assert sum(find_valid_games(SAMPLE_INPUT)) == 8


GAME_POWER_TEST_CASES = (
    ("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green", 48),
    ("Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue", 12),
    ("Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red", 1560),
    ("Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red", 630),
    ("Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green", 36),
)


@pytest.mark.parametrize(("game_spec", "truth_power"), GAME_POWER_TEST_CASES)
def test_game_power(game_spec: str, truth_power: int) -> None:
    g = Game(game_spec)
    assert g.power == truth_power
