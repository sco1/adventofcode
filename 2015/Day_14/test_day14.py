import typing as t
from textwrap import dedent

import pytest
from aoc_2015_day14 import Reindeer, ReindeerRace

PUZZLE_INPUT = dedent(
    """\
    Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
    Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.
    """
)


class RaceTestCase(t.NamedTuple):
    """Represent a snapshot of the race after a certain number of seconds have elapsed."""

    elapsed_seconds: int
    comet_distance: int
    dancer_distance: int


RACE_CASES = [
    RaceTestCase(1, 14, 16),
    RaceTestCase(10, 140, 160),
    RaceTestCase(11, 140, 176),
    RaceTestCase(12, 140, 176),
    RaceTestCase(138, 154, 176),
    RaceTestCase(1000, 1120, 1056),
]

REINDEER = [Reindeer.from_puzzle_input(line) for line in PUZZLE_INPUT.splitlines()]
RACE = ReindeerRace(REINDEER)


@pytest.mark.parametrize("elapsed_seconds,comet_distance,dancer_distance", RACE_CASES)
def test_reindeer_race(elapsed_seconds: int, comet_distance: int, dancer_distance: int) -> None:
    """Check the reindeer positions after the specified number of seconds have elapsed."""
    RACE.restart()
    RACE.step_n(elapsed_seconds)

    assert RACE.reindeer[0].distance == comet_distance
    assert RACE.reindeer[1].distance == dancer_distance


class PointsTestCase(t.NamedTuple):
    """Represent a snapshot of the race after a certain number of seconds have elapsed."""

    elapsed_seconds: int
    comet_points: int
    dancer_points: int


POINTS_CASES = [
    PointsTestCase(1, 0, 1),
    PointsTestCase(140, 1, 139),
    PointsTestCase(1000, 312, 689),
]


@pytest.mark.parametrize("elapsed_seconds,comet_points,dancer_points", POINTS_CASES)
def test_reindeer_points(elapsed_seconds: int, comet_points: int, dancer_points: int) -> None:
    """Check the reindeer points after the specified number of seconds have elapsed."""
    RACE.restart()
    RACE.step_n(elapsed_seconds)

    assert RACE.reindeer[0].points == comet_points
    assert RACE.reindeer[1].points == dancer_points
