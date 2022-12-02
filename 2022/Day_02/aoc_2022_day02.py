from functools import cache
from pathlib import Path

# Opponent: A - Rock, B - Paper, C - Scissors
# Self:     X - Rock, Y - Paper, Z - Scissors
WINS = {"A Y", "B Z", "C X"}  # Gain 6 points
LOSES = {"A Z", "B X", "C Y"}  # Gain 0 points
DRAWS = {"A X", "B Y", "C Z"}  # Gain 3 points

POINTS = {
    "X": 1,
    "Y": 2,
    "Z": 3,
}


@cache
def score_round(game_round: str) -> int:
    """
    Calculate the score for the given round of RPS.

    The round's score is calculated by summing the hand played by the player (the second letter) and
    the result of the round, where win = `6`, draw = `3`, and loss = `0`.
    """
    _, me = game_round.split()
    score = POINTS.get(me)

    if score is None:
        raise ValueError(f"Unknown shape played by player: '{me}'")

    if game_round in WINS:
        score += 6
    elif game_round in LOSES:
        score += 0
    elif game_round in DRAWS:
        score += 3
    else:
        raise ValueError(f"Unknown game round encountered: '{game_round}'")

    return score


def score_game(strategy_guide: str) -> int:
    """Calculate the total game score where each line of the guide is the shape to play."""
    return sum(score_round(round) for round in strategy_guide.splitlines())


def _find_shape(opponent: str, moveset: set[str]) -> str:
    """Determine which shape I need to play to satisfy the provided round outcome."""
    for move in ("X", "Y", "Z"):
        if f"{opponent} {move}" in moveset:
            return move

    raise ValueError("Could not identify a move satisfying the provided play conditions.")


@cache
def score_perfect_round(game_round: str) -> int:
    """
    Calculate the score for the given round of RPS using the "perfect" strategy.

    Rounds are determined based on the opponent's hand and the the strategy instruction, where `X`
    is a loss, `Y` is a draw, and `Z` is a win.
    """
    # For each round, figure out what shape I need to play to win
    # This is a stupid way to do it vs. just hardcoding the combinations, but it's fun!
    opponent, outcome = game_round.split()
    if outcome == "X":
        should_play = _find_shape(opponent, LOSES)
    elif outcome == "Y":
        should_play = _find_shape(opponent, DRAWS)
    elif outcome == "Z":
        should_play = _find_shape(opponent, WINS)
    else:
        raise ValueError(f"Unknown outcome provided: '{outcome}'")

    return score_round(f"{opponent} {should_play}")


def score_perfect_strat(strategy_guide: str) -> int:
    """Calculate the total game score where each line of the guide is the round outcome."""
    return sum(score_perfect_round(round) for round in strategy_guide.splitlines())


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text()

    print(f"Part One: {score_game(puzzle_input)}")
    print(f"Part Two: {score_perfect_strat(puzzle_input)}")
