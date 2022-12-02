from textwrap import dedent

import pytest

from .aoc_2022_day02 import (
    DRAWS,
    LOSES,
    WINS,
    _find_shape,
    score_game,
    score_perfect_strat,
    score_round,
)

SAMPLE_SCORES = (
    ("A Y", 8),
    ("B X", 1),
    ("C Z", 6),
)


@pytest.mark.parametrize(("round", "truth_score"), SAMPLE_SCORES)
def test_round_score(round: str, truth_score: int) -> None:
    assert score_round(round) == truth_score


SAMPLE_GAME = dedent(
    """\
    A Y
    B X
    C Z
    """
)


def test_total_score() -> None:
    assert score_game(SAMPLE_GAME) == 15


SAMPLE_PERFECT_STRATS = (
    ("A", DRAWS, "X"),
    ("A", WINS, "Y"),
    ("A", LOSES, "Z"),
    ("B", LOSES, "X"),
    ("C", WINS, "X"),
)


@pytest.mark.parametrize(("opponent", "moveset", "should_play"), SAMPLE_PERFECT_STRATS)
def test_find_shape(opponent: str, moveset: set[str], should_play: str) -> None:
    assert _find_shape(opponent, moveset) == should_play


def test_perfect_strat() -> None:
    assert score_perfect_strat(SAMPLE_GAME) == 12
