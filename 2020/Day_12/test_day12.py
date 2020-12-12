from textwrap import dedent

from .aoc_2020_day12 import AdventFerry


SAMPLE_INSTRUCTIONS = dedent(
    """\
    F10
    N3
    F7
    R90
    F11
    """
)


def test_ferry_driving() -> None:
    """Test Part 1, where the instructions drive the ship itself."""
    advent_cruise = AdventFerry(SAMPLE_INSTRUCTIONS)
    advent_cruise.run()

    assert advent_cruise.distance_from_start() == 25


def test_waypoint_driving() -> None:
    """Test Part 2, where the instructions manipulate the ship's steering waypoint."""
    advent_cruise = AdventFerry(SAMPLE_INSTRUCTIONS, waypoint_mode=True)
    advent_cruise.run()

    assert advent_cruise.distance_from_start() == 286
