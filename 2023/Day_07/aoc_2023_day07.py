from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from enum import IntEnum
from pathlib import Path


# Best hand to worst hand
class HandType(IntEnum):  # noqa: D101
    FIVE_K = 6
    FOUR_K = 5
    FULL_HOUSE = 4
    THREE_K = 3
    TWO_PAIR = 2
    PAIR = 1
    HIGH_CARD = 0


# Map sorted(Counter.values()) to the appropriate hand
HAND_MAPPING = {
    (5,): HandType.FIVE_K,
    (1, 4): HandType.FOUR_K,
    (2, 3): HandType.FULL_HOUSE,
    (1, 1, 3): HandType.THREE_K,
    (1, 2, 2): HandType.TWO_PAIR,
    (1, 1, 1, 2): HandType.PAIR,
    (1, 1, 1, 1, 1): HandType.HIGH_CARD,
}

# Since we only have 5 cards we can just enumerate the possible best hand types by including the
# number of jokers in the key
HAND_MAPPING_JOKERS = {
    (0, (5,)): HandType.FIVE_K,
    (5, (5,)): HandType.FIVE_K,
    (1, (1, 4)): HandType.FIVE_K,
    (2, (2, 3)): HandType.FIVE_K,
    (3, (2, 3)): HandType.FIVE_K,
    (4, (1, 4)): HandType.FIVE_K,
    (0, (1, 4)): HandType.FOUR_K,
    (1, (1, 1, 3)): HandType.FOUR_K,
    (2, (1, 2, 2)): HandType.FOUR_K,
    (3, (1, 1, 3)): HandType.FOUR_K,
    (0, (2, 3)): HandType.FULL_HOUSE,
    (1, (1, 2, 2)): HandType.FULL_HOUSE,
    (0, (1, 1, 3)): HandType.THREE_K,
    (1, (1, 1, 1, 2)): HandType.THREE_K,
    (2, (1, 1, 1, 2)): HandType.THREE_K,
    (0, (1, 2, 2)): HandType.TWO_PAIR,
    (0, (1, 1, 1, 2)): HandType.PAIR,
    (1, (1, 1, 1, 1, 1)): HandType.PAIR,
    (0, (1, 1, 1, 1, 1)): HandType.HIGH_CARD,
}

# Individual card values to use for tiebreaking
CARD_VAL = {c: v for v, c in enumerate("23456789TJQKA")}
JOKER_CARD_VAL = {c: v for v, c in enumerate("J23456789TQKA")}


@dataclass
class Player:
    """
    Represent a player's hand in a round of Camel Cards.

    This class supports sorting by the hierarchy enumerated by `HandType`. If hands are of the same
    type, ties are broken by comparing the card at each position in the hand until a winner is found
    """

    hand: Counter[str]
    hand_type: HandType
    bid: int

    _card_vals: tuple[int, ...]

    @classmethod
    def from_str(cls, player_spec: str, count_jokers: bool = False) -> Player:
        """
        Parse the Camel Cards hand from the provided raw specification.

        Hands are assumed to be provided as `<cards> <bid>`, where cards is a 5-card hand specified
        as `1-9`, or `TJQK`. The hand is followed by its bid amount, assumed to be specified as an
        integer.

        If `count_jokers` is `True`, `J` cards are assumed to be Jokers instead of Jacks. Jokers are
        wildcards that can act like whatever card would make the given hand the strongest type
        possible. To balance this power, `J` cards are now the weakest card when being considered
        as a tie-breaker.
        """
        raw_hand, raw_bid = (half.strip() for half in player_spec.split())
        hand = Counter(raw_hand)

        if count_jokers:
            n_jokers = hand.get("J", 0)
            hand_type = HAND_MAPPING_JOKERS[(n_jokers, tuple(sorted(hand.values())))]
            card_vals = tuple(JOKER_CARD_VAL[c] for c in raw_hand)
        else:
            hand_type = HAND_MAPPING[tuple(sorted(hand.values()))]
            card_vals = tuple(CARD_VAL[c] for c in raw_hand)

        return Player(hand=hand, hand_type=hand_type, bid=int(raw_bid), _card_vals=card_vals)

    def __lt__(self, other: Player) -> bool:
        if self.hand_type != other.hand_type:
            return self.hand_type < other.hand_type
        else:
            return self._card_vals < other._card_vals


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    players = [Player.from_str(line) for line in puzzle_input.splitlines()]
    print(f"Part One: {sum((rank * p.bid) for rank, p in enumerate(sorted(players), start=1))}")

    players = [Player.from_str(line, count_jokers=True) for line in puzzle_input.splitlines()]
    print(f"Part Two: {sum((rank * p.bid) for rank, p in enumerate(sorted(players), start=1))}")
