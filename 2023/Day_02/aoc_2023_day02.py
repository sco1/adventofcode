import math
from collections import defaultdict
from enum import StrEnum, auto
from pathlib import Path


class Color(StrEnum):  # noqa: D101
    RED = auto()
    BLUE = auto()
    GREEN = auto()


class Game:  # noqa: D101
    game_no: int
    rounds: list[dict[Color, int]]
    most_seen: dict[Color, int]

    def __init__(self, description: str) -> None:
        self.rounds = []
        self.most_seen = defaultdict(int)

        self.parse_description(description)

    @property
    def power(self) -> int:
        """
        Calculate the power of the minimum set of cubes required to make the current game possible.

        The power of a set of cubes is equal to the product of the quantities of each color cube.
        """
        return math.prod(self.most_seen.values())

    def parse_description(self, description: str) -> None:
        """
        Parse the provided game description into its component information.

        The game description is assumed to be of the form:
            `Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green`

        The description begins by identifying the game ID number followed by a semicolon-separated
        list of game rounds. For each game round, the Elf reaches into the bag and reveals a random
        number of colored cubes.

        After parsing all rounds, the `most_seen` dictionary is updated with the maximum number of
        each color cube seen over the course of the game.
        """
        if not description.startswith("Game"):
            raise ValueError(f"Unknown description provided: '{description}'")

        game_spec, rounds_spec = description.split(":")
        self.game_no = int(game_spec.split()[-1])

        for round_s in rounds_spec.split(";"):
            game_round = defaultdict(int)
            for grab in round_s.split(","):
                block_n, block_color = (c.strip() for c in grab.split())
                game_round[Color(block_color)] = int(block_n)

                self.most_seen[Color(block_color)] = max(
                    self.most_seen[Color(block_color)], int(block_n)
                )

            self.rounds.append(game_round)

    def is_possible(self, red: int, green: int, blue: int) -> bool:
        """Determine if the game is possible using the specified set of color cube quantities."""
        return all(
            (
                self.most_seen[Color.RED] <= red,
                self.most_seen[Color.GREEN] <= green,
                self.most_seen[Color.BLUE] <= blue,
            )
        )


def find_valid_games(description: str, query_bag: tuple[int, int, int] = (12, 13, 14)) -> list[int]:
    """
    Find the IDs of the games possible as described using the specified bag of cubes.

    `query_bag` is a bag of cubes whose contents are specified as a (red, green, blue) tuple.

    A game is possible as described if it does not attempt to show more cubes of a specific color
    than is contained by the query bag.
    """
    red, green, blue = query_bag

    valid_games = []
    for line in description.splitlines():
        g = Game(line)
        if g.is_possible(red=red, green=green, blue=blue):
            valid_games.append(g.game_no)

    return valid_games


def calculate_total_power(description: str) -> int:
    """
    Calculate the sum of powers for the provided set of cube games.

    The power of a set of cubes is equal to the product of the number of each color cube required to
    make the described game possible.
    """
    return sum(Game(line).power for line in description.splitlines())


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    print(f"Part One: {sum(find_valid_games(puzzle_input))}")
    print(f"Part Two: {calculate_total_power(puzzle_input)}")
