from helpers.parsing import parse_hashed_map
from .aoc_2025_day04 import find_accessible_rolls, remove_all_accessible

SAMPLE_MAP = """\
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
"""


def test_find_accessible_rolls() -> None:
    ROLL_LOCATIONS = parse_hashed_map(SAMPLE_MAP, marker="@")
    assert len(find_accessible_rolls(ROLL_LOCATIONS)) == 13


def test_remove_all_accessible() -> None:
    ROLL_LOCATIONS = parse_hashed_map(SAMPLE_MAP, marker="@")
    assert remove_all_accessible(ROLL_LOCATIONS) == 43
