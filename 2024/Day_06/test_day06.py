from textwrap import dedent

from helpers.geometry import BoundingBox
from .aoc_2024_day06 import parse_lab_map, trap_guard, walk_patrol

SAMPLE_INPUT = dedent(
    """\
    ....#.....
    .........#
    ..........
    ..#.......
    .......#..
    ..........
    .#..^.....
    ........#.
    #.........
    ......#...
    """
)
TRUTH_START_LOC = (4, 6)
TRUTH_OBSTRUCTIONS = {(4, 0), (9, 1), (2, 3), (7, 4), (1, 6), (8, 7), (0, 8), (6, 9)}
TRUTH_BBOX = BoundingBox(((0, 0), (0, 9), (9, 0), (9, 9)))


def test_parse_lab_map() -> None:
    start_loc, obstructions, lab_bbox = parse_lab_map(SAMPLE_INPUT)

    assert start_loc == TRUTH_START_LOC
    assert obstructions == TRUTH_OBSTRUCTIONS
    assert lab_bbox == TRUTH_BBOX


def test_walk_lab_map() -> None:
    assert len(walk_patrol(*parse_lab_map(SAMPLE_INPUT))) == 41


def test_trap_guard() -> None:
    assert len(trap_guard(*parse_lab_map(SAMPLE_INPUT))) == 6
