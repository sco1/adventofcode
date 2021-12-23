import pytest

from .aoc_2021_day17 import find_highest_y, n_valid_launches, parse_target_area

SAMPLE_AREAS = [
    ("target area: x=20..30, y=-10..-5", (20, 30, -10, -5)),
    ("target area: x=14..50, y=-267..-225", (14, 50, -267, -225)),
]


@pytest.mark.parametrize(("target_area", "truth_bounds"), SAMPLE_AREAS)
def test_area_parsing(target_area: str, truth_bounds: tuple[int, int, int, int]) -> None:
    assert parse_target_area(target_area) == truth_bounds


SAMPLE_INPUT = "target area: x=20..30, y=-10..-5"
TARGET_AREA = parse_target_area(SAMPLE_INPUT)


def test_part_one() -> None:
    assert find_highest_y(TARGET_AREA) == 45


def test_part_two() -> None:
    assert n_valid_launches(TARGET_AREA) == 112
