from textwrap import dedent

from .aoc_2021_day21 import DiracDice, get_starting_positions, play_quantum

SAMPLE_INPUT = dedent(
    """\
    Player 1 starting position: 4
    Player 2 starting position: 8
    """
)


def test_part_one() -> None:
    game = DiracDice.from_puzzle_input(SAMPLE_INPUT)
    assert game.play_determinstic() == 739_785


def test_part_two() -> None:
    assert max(play_quantum(*get_starting_positions(SAMPLE_INPUT))) == 444_356_092_776_315
