from textwrap import dedent

from .aoc_2018_day6 import (
    build_distance_map,
    find_finite_areas,
    find_safe_region,
    parse_coordinates,
)

SAMPLE_COORDINATES = dedent(
    """\
    1, 1
    1, 6
    8, 3
    3, 4
    5, 5
    8, 9
    """
)


def test_finite_areas() -> None:
    coords, bbox = parse_coordinates(SAMPLE_COORDINATES)
    distance_map = build_distance_map(coords, bbox)
    finite_areas = find_finite_areas(distance_map, bbox)

    assert finite_areas == [9, 17]


def test_safe_region() -> None:
    coords, bbox = parse_coordinates(SAMPLE_COORDINATES)
    assert len(find_safe_region(coords, bbox, safe_dist=32)) == 16
