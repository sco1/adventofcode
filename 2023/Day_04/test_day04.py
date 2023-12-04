from textwrap import dedent

import pytest

from .aoc_2023_day04 import Card, modified_bulk_score

CARD_SCORE_CASES = (
    ("Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53", 4, 8),
    ("Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19", 2, 2),
    ("Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1", 2, 2),
    ("Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83", 1, 1),
    ("Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36", 0, 0),
    ("Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11", 0, 0),
)


@pytest.mark.parametrize(("card_spec", "truth_n_matching", "truth_score"), CARD_SCORE_CASES)
def test_card_parsing(card_spec: str, truth_n_matching: int, truth_score: int) -> None:
    card = Card.from_str(card_spec)
    assert len(card.matches) == truth_n_matching
    assert card.value == truth_score


SAMPLE_CARDS = dedent(
    """\
    Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
    Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
    Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
    Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
    Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
    Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
    """
)


def test_bulk_score() -> None:
    cards = [Card.from_str(line) for line in SAMPLE_CARDS.splitlines()]
    assert sum(card.value for card in cards) == 13


TRUTH_CARD_COUNDS_PT2 = {
    1: 1,
    2: 2,
    3: 4,
    4: 8,
    5: 14,
    6: 1,
}


def test_modified_bulk_score() -> None:
    cards = [Card.from_str(line) for line in SAMPLE_CARDS.splitlines()]
    score, card_counts = modified_bulk_score(cards)

    assert score == 30
    assert card_counts == TRUTH_CARD_COUNDS_PT2
