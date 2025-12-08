from helpers.geometry import BoundingBox
from .aoc_2025_day07 import fire_beam, parse_diagram

SAMPLE_INPUT = """\
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
"""
TRUTH_START = (7, 0)
TRUTH_SPLITTERS = {
    (1, 14),
    (2, 12),
    (3, 10),
    (3, 14),
    (4, 8),
    (5, 6),
    (5, 10),
    (5, 14),
    (6, 4),
    (6, 8),
    (6, 12),
    (7, 2),
    (7, 6),
    (7, 14),
    (8, 4),
    (9, 6),
    (9, 10),
    (9, 14),
    (10, 8),
    (11, 10),
    (12, 12),
    (13, 14),
}
TRUTH_BBOX = BoundingBox.from_dims(width=15, height=16)


def test_parse_diagram() -> None:
    start, splitters, bbox = parse_diagram(SAMPLE_INPUT)

    assert start == TRUTH_START
    assert splitters == TRUTH_SPLITTERS
    assert bbox == TRUTH_BBOX


def test_n_splits() -> None:
    n_splits, _ = fire_beam(TRUTH_START, TRUTH_SPLITTERS, TRUTH_BBOX)

    assert n_splits == 21


def test_n_timelines() -> None:
    _, n_timelines = fire_beam(TRUTH_START, TRUTH_SPLITTERS, TRUTH_BBOX)

    assert n_timelines == 40
