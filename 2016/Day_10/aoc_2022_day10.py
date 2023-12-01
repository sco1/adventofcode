from __future__ import annotations

import math
import re
import typing as t
from collections import defaultdict, deque
from pathlib import Path


class HasChips(t.Protocol):  # noqa: D101
    chips: list[int]


class Output:  # noqa: D101
    chips: list[int]

    def __init__(self) -> None:
        self.chips = []


class Bot:  # noqa: D101
    chips: list[int]
    give_low: HasChips
    give_high: HasChips

    last_compared = tuple[int, int]

    def __init__(self) -> None:
        self.chips = []


class Factory:  # noqa: D101
    bots: dict[int, Bot]
    outputs: dict[int, Output]

    def __init__(self, instructions: str) -> None:
        self.bots = defaultdict(Bot)
        self.outputs = defaultdict(Output)
        self.parse_instructions(instructions)

        self.run()

    def parse_instructions(self, instructions: str) -> None:
        """
        Parse the provided factory instructions & initialize the factory's components.

        Each line is assumed to be a single instruction of one of the following forms:
            * `value <A> goes to bot <B>`
            * `bot <A> gives low to <bot/output> <B> and high to <bot|output> <C>`

        It is assumed that at the end of parsing all robots have been assigned a destination for
        their high and low microchip values, and have an inventory of zero to two chips, inclusive.
        """
        for line in instructions.splitlines():
            if line.startswith("value"):
                chip, bot_id = (int(v) for v in re.findall(r"\d+", line))
                self.bots[bot_id].chips.append(chip)
            elif line.startswith("bot"):
                source, give_low, give_high = re.findall(r"bot \d+|output \d+", line)

                source_id = int(source.split()[-1])

                low_dest, low_id = give_low.split()
                if low_dest == "bot":
                    self.bots[source_id].give_low = self.bots[int(low_id)]
                elif low_dest == "output":
                    self.bots[source_id].give_low = self.outputs[int(low_id)]
                else:
                    raise ValueError(f"Unknown destination: '{low_dest}'")

                high_dest, high_id = give_high.split()
                if high_dest == "bot":
                    self.bots[source_id].give_high = self.bots[int(high_id)]
                elif high_dest == "output":
                    self.bots[source_id].give_high = self.outputs[int(high_id)]
                else:
                    raise ValueError(f"Unknown destination: '{high_dest}'")

    @property
    def pending_bots(self) -> list[Bot]:
        """Return a list of bots in posession of two microchips."""
        return [bot for bot in self.bots.values() if len(bot.chips) == 2]

    def run(self) -> None:
        """Iterate through all bots until no bot has more than 1 chip in their posession."""
        run_queue = deque(self.pending_bots)
        while run_queue:
            bot = run_queue.popleft()
            if len(bot.chips) != 2:
                continue

            bot.chips.sort()
            bot.last_compared = tuple(bot.chips)

            bot.give_high.chips.append(bot.chips.pop())
            bot.give_low.chips.append(bot.chips.pop())

            run_queue.extend(self.pending_bots)

    def who_compared(self, chip_pair: tuple[int, int]) -> int | None:
        """Identify the bot who last compared the two chps specified by `chip_pair`."""
        chip_pair = tuple(sorted(chip_pair))  # type: ignore[assignment]
        for idx, bot in self.bots.items():
            if bot.last_compared == chip_pair:
                return idx

        return None


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    fact = Factory(puzzle_input)
    print(f"Part One: {fact.who_compared((61, 17))}")
    print(f"Part Two: {math.prod((fact.outputs[idx].chips[0] for idx in (0, 1, 2)))}")
