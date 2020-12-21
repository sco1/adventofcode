import typing as t
from collections import defaultdict, deque
from functools import partial
from pathlib import Path


SEEN_DEQUE = partial(deque, maxlen=2)


class NumberGame:
    """
    Represent an instance of the Elves' memory game.

    For this game, players take turns saying numbers. First, they begin by reading through the
    list of starting numbers, then the number for each turn considers the most recently spoken
    number:
        * If that was the first time the number has been spoken, the current player says `0`
        * Otherwise, the number had been spoken before; the current player announces how many turns
        apart the number is from when it was previously spoken
    """

    step: int
    last_seen: int
    seen_cache: dict[int, t.Deque]

    def __init__(self, starting_numbers: str) -> None:
        self.step = 1
        self.seen_cache = defaultdict(SEEN_DEQUE)
        self.starting_numbers = deque(int(n) for n in starting_numbers.split(","))

    def step_game(self) -> None:
        """Advance the game by a single step."""
        # Go through the starting numbers before checking for numbers we've seen
        if self.starting_numbers:
            self.last_seen = self.starting_numbers.popleft()
            self.seen_cache[self.last_seen].append(self.step)
            self.step += 1
            return

        # Starting numbers have been exhausted, now check for repeat numbers
        seen_steps = self.seen_cache[self.last_seen]
        if len(seen_steps) == 1:
            self.last_seen = (self.step - 1) - seen_steps[0]
        else:
            self.last_seen = seen_steps[1] - seen_steps[0]

        self.seen_cache[self.last_seen].append(self.step)
        self.step += 1

    def step_n(self, n_steps: int = 2020) -> None:
        """Batch advance the game by `n_steps`."""
        for _ in range(n_steps):
            self.step_game()


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    game = NumberGame(puzzle_input)
    game.step_n(2020)
    print(f"Part One: {game.last_seen}")

    game = NumberGame(puzzle_input)
    game.step_n(30_000_000)
    print(f"Part Two: {game.last_seen}")
