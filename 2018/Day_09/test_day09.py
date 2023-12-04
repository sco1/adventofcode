import pytest

from .aoc_2018_day9 import play_game


SAMPLE_GAME_SCORES = (
    (10, 1_618, 8_317),
    (13, 7_999, 146_373),
    (17, 1_104, 2_764),
    (21, 6_111, 54_718),
    (30, 5_807, 37_305),
)

@pytest.mark.parametrize(("n_players", "n_marbles", "truth_score"), SAMPLE_GAME_SCORES)
def test_marble_scoring(n_players: int, n_marbles: int, truth_score: int) -> None:
    assert play_game(n_players, n_marbles) == truth_score
