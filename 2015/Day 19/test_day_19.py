import typing as t
from textwrap import dedent

import pytest
from aoc_2015_day_19 import count_unique_products, parse_input


class ReactionTestCase(t.NamedTuple):
    puzzle_input: str
    n_expected_outputs: int


REACTION_CASES = [
    ReactionTestCase(
        dedent(
            """\
            H => HO
            H => OH
            O => HH

            HOH
            """
        ),
        4,
    ),
    ReactionTestCase(
        dedent(
            """\
            H => HO
            H => OH
            O => HH

            HOHOHO
            """
        ),
        7,
    ),
    ReactionTestCase(
        dedent(
            """\
            H => OO

            H2O
            """
        ),
        1,
    ),
]


@pytest.mark.parametrize("puzzle_input,n_expected_outputs", REACTION_CASES)
def test_reactions(puzzle_input: str, n_expected_outputs: int) -> None:
    """"""
    reactions, starting_molecule = parse_input(puzzle_input.splitlines())
    assert count_unique_products(reactions, starting_molecule) == n_expected_outputs
