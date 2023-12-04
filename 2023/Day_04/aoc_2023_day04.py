from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Card:  # noqa: D101
    id: int
    winning_numbers: set[int]
    my_numbers: set[int]

    matches: set[int] = field(init=False)
    value: int = field(init=False)

    def __post_init__(self) -> None:
        """
        Calculate the card's score based on the winning & scratched numbers.

        If one or more numbers match, the first match is worth 1 point, then the total score is
        doubled for each additional match.
        """
        self.matches = self.winning_numbers & self.my_numbers
        if self.matches:
            self.value = 2 ** (len(self.matches) - 1)
        else:
            self.value = 0

    @classmethod
    def from_str(cls, raw_card: str) -> Card:
        """
        Parse the provided scratch card description.

        Cards are assumed be described in the form `Card <id>: <winning numbers> | <my numbers>`,
        where numbers are a series of one or more space separated integers.
        """
        card_spec, nums = raw_card.split(":")
        card_id = int(re.findall(r"\d+", card_spec)[0])

        winning_raw, my_raw = nums.split("|")
        winning = {int(n) for n in winning_raw.split()}
        mine = {int(n) for n in my_raw.split()}

        return Card(card_id, winning, mine)


def modified_bulk_score(cards: list[Card]) -> tuple[int, dict[int, int]]:
    """
    Calculate the bulk score for the provided collection of scratchcards.

    For each winning card, you win copies of the scratchcards below the winning card equal to the
    number of matches. For example, if card `10` were to have `5` matching numbers, you would win
    one copy each of cards `11`, `12`, `13`, `14`, and `15`; this process is recursive, so if you
    have two copies of card `10`, you receive two copies of each of these cards.

    NOTE: It is assumed that the card with the highest ID number does not have any matching numbers.
    """
    card_counts = {card.id: 1 for card in cards}
    for card in cards:
        for n in range(card.id, card.id + len(card.matches)):
            card_counts[n + 1] += card_counts[card.id]

    return sum(card_counts.values()), card_counts


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    cards = [Card.from_str(line) for line in puzzle_input.splitlines()]
    print(f"Part One: {sum(card.value for card in cards)}")
    print(f"Part Two: {modified_bulk_score(cards)[0]}")
