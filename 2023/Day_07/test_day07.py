from textwrap import dedent

import pytest

from .aoc_2023_day07 import HandType, Player

PLAYER_CASES = (
    ("32T3K 765", HandType.PAIR, 765),
    ("T55J5 684", HandType.THREE_K, 684),
    ("KK677 28", HandType.TWO_PAIR, 28),
    ("KTJJT 220", HandType.TWO_PAIR, 220),
    ("QQQJA 483", HandType.THREE_K, 483),
)


@pytest.mark.parametrize(("player_spec", "truth_kind", "truth_bid"), PLAYER_CASES)
def test_hand_parsing(player_spec: str, truth_kind: HandType, truth_bid: int) -> None:
    p = Player.from_str(player_spec)
    assert p.hand_type == truth_kind
    assert p.bid == truth_bid


SAMPLE_INPUT = dedent(
    """\
    32T3K 765
    T55J5 684
    KK677 28
    KTJJT 220
    QQQJA 483
    """
)

TRUTH_RANKING = (1, 4, 3, 2, 5)
TRUTH_WINNINGS = 6440


def test_hand_ranking() -> None:
    players = [Player.from_str(line) for line in SAMPLE_INPUT.splitlines()]

    sorted_players = sorted(
        ((idx, p) for idx, p in enumerate(players, start=1)), key=lambda x: x[1]
    )
    assert tuple(idx for idx, _ in sorted_players) == TRUTH_RANKING

    assert sum((rank * p.bid) for rank, p in enumerate(sorted(players), start=1)) == TRUTH_WINNINGS


TRUTH_RANKING_JOKERS = (1, 3, 2, 5, 4)
TRUTH_WINNINGS_JOKERS = 5905


def test_hand_ranking_jokers() -> None:
    players = [Player.from_str(line, count_jokers=True) for line in SAMPLE_INPUT.splitlines()]

    sorted_players = sorted(
        ((idx, p) for idx, p in enumerate(players, start=1)), key=lambda x: x[1]
    )
    assert tuple(idx for idx, _ in sorted_players) == TRUTH_RANKING_JOKERS

    assert (
        sum((rank * p.bid) for rank, p in enumerate(sorted(players), start=1))
        == TRUTH_WINNINGS_JOKERS
    )
