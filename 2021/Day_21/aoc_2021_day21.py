from __future__ import annotations

import functools
import itertools as it
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

N_SPACES = 10

MAX_QUANTUM_SCORE = 21
N_QUANTUM_SIDES = 3
N_QUANTUM_ROLLS = 3
# Count the number of ways we can roll each possible combination of dice
QUANTUM_OUTCOMES = Counter(
    sum(rolls) for rolls in it.product(range(1, N_QUANTUM_SIDES + 1), repeat=N_QUANTUM_ROLLS)
)


def get_starting_positions(puzzle_input: str) -> list[int]:
    """
    Parse the provided player starting positions.

    Player starting positions are assumed to be given in the form:
        * `"Player <n> starting position: <x>"`

    NOTE: Starting positions are assumed to be given as 1-indexed & are converted to 0-indexed.
    """
    return [int(re.findall(r"\d+", line)[1]) - 1 for line in puzzle_input.splitlines()]


@dataclass
class Player:  # noqa: D101
    position: int  # Zero-indexed
    score: int = 0


@dataclass
class DiracDice:  # noqa: D101
    player1: Player
    player2: Player

    n_spaces: int = N_SPACES
    max_score: int = 1000
    n_sides = 100

    _current_roll: int = 0
    _n_rolls: int = 0

    def roll(self) -> int:
        """Roll the dice!"""
        self._n_rolls += 1
        # We're assuming the die is deterministic
        self._current_roll = (self._current_roll + 1) % self.n_sides
        return self._current_roll

    def play_determinstic(self) -> int:
        """
        Play a DiracDice using a 100-sided deterministic die.

        Players take turns moving. On each player's turn, the player rolls the die three times and
        adds up the results. Then, the player moves their pawn that many times forward around the
        track (that is, moving clockwise on spaces in order of increasing value, wrapping back
        around to 1 after 10). After each player moves, they increase their score by the value of
        the space their pawn stopped on.

        Players take turns until they reach the max score; once a player reaches the max score,
        the game's final score is calculated by multiplying the losing player's score score and the
        total number of dice rolls.
        """
        while True:
            move = sum((self.roll() for _ in range(3)))
            self.player1.position = (self.player1.position + move) % self.n_spaces
            self.player1.score += self.player1.position + 1

            if self.player1.score >= self.max_score:
                return self.player2.score * self._n_rolls

            move = sum((self.roll() for _ in range(3)))
            self.player2.position = (self.player2.position + move) % self.n_spaces
            self.player2.score += self.player2.position + 1

            if self.player2.score >= self.max_score:
                return self.player1.score * self._n_rolls

    @classmethod
    def from_puzzle_input(cls, puzzle_input: str) -> DiracDice:
        """
        Initialize a dice game from the provided starting positions for Player 1 & Player 2.

        Player starting positions are assumed to be given in the form:
            * `"Player <n> starting position: <x>"`

        NOTE: Starting positions are assumed to be given as 1-indexed & are converted to 0-indexed.
        """
        start_positions = get_starting_positions(puzzle_input)
        return cls(Player(start_positions[0]), Player(start_positions[1]))


# Rather than make some OOP based monstrosity for Part 2, let's go with some recursion to keep
# myself marginally more sane
@functools.cache
def play_quantum(
    curr_player_pos: int,
    next_player_pos: int,
    curr_player_score: int = 0,
    next_player_score: int = 0,
) -> tuple[int, int]:
    """
    Simulate a game of Dirac dice played using dice from the quantum realm!

    When a quantum die is rolled, the universe splits into multiple copies, one copy for each
    possible outcome of the die. In this case, rolling the die always splits the universe into three
    copies: one where the outcome of the roll was `1`, one where it was `2`, and one where it was
    `3`.

    Using the provided starting positions, every possible outcome is determined and the number of
    wins for each player is provided.

    NOTE: Player positions are assumed to be 0-indexed.
    """
    # Since the game is symmetric and there are only 2 players, we can just swap players as we
    # recurse & not have to also keep track of which player is currently playing.
    # As we recurse, we're receiving the previous player's score as next_player_score, so if that
    # player has won then we can stop playing
    if next_player_score >= MAX_QUANTUM_SCORE:
        return 0, 1

    n_wins_curr = n_wins_next = 0
    for roll, n_combinations in QUANTUM_OUTCOMES.items():
        # Rather than brute force through every possible dice roll, we can more gracefully force our
        # way through each possible combination & multiply the individual outcome by the number of
        # times its respective dice roll will show up.
        new_pos = (curr_player_pos + roll) % N_SPACES
        next_wins, current_wins = play_quantum(
            next_player_pos, new_pos, next_player_score, curr_player_score + (new_pos + 1)
        )

        n_wins_curr += (n_combinations * current_wins)
        n_wins_next += (n_combinations * next_wins)

    # Once we finish recursing through everything, we will get back Player 1's wins, then Player 2's
    return n_wins_curr, n_wins_next


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text()

    game = DiracDice.from_puzzle_input(puzzle_input)
    print(f"Part One: {game.play_determinstic()}")
    print(f"Part Two: {max(play_quantum(*get_starting_positions(puzzle_input)))}")
