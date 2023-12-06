import dataclasses
from textwrap import dedent

import pytest

from .aoc_2023_day06 import RaceSpec, winning_strategies

SAMPLE_INPUT = dedent(
    """\
    Time:      7  15   30
    Distance:  9  40  200
    """
)

TRUTH_SPECS = (
    (7, 9),
    (15, 40),
    (30, 200),
)


def test_race_spec_parsing() -> None:
    specs = RaceSpec.from_race_document(SAMPLE_INPUT)
    for spec, truth_spec in zip(specs, TRUTH_SPECS):
        assert dataclasses.astuple(spec) == truth_spec


def test_race_spec_parsing_bad_kerning() -> None:
    spec = RaceSpec.from_race_document(SAMPLE_INPUT, ignore_spaces=True)[0]
    assert dataclasses.astuple(spec) == (71530, 940_200)


WINNING_STRATEGY_CASES = (
    (RaceSpec(race_time=7, distance_record=9), [2, 3, 4, 5]),
    (RaceSpec(race_time=15, distance_record=40), [4, 5, 6, 7, 8, 9, 10, 11]),
    (RaceSpec(race_time=30, distance_record=200), [11, 12, 13, 14, 15, 16, 17, 18, 19]),
)


@pytest.mark.parametrize(("race_spec", "truth_strategies"), WINNING_STRATEGY_CASES)
def test_winning_strategies(race_spec: RaceSpec, truth_strategies: list[int]) -> None:
    assert winning_strategies(race_spec) == truth_strategies


def test_long_race() -> None:
    spec = RaceSpec.from_race_document(SAMPLE_INPUT, ignore_spaces=True)[0]
    assert len(winning_strategies(spec)) == 71_503
