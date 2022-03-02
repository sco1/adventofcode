from textwrap import dedent

from .aoc_2018_day6 import _parse_coordinates

SAMPLE_COORDINATES = dedent(
    """\
    1, 1
    1, 6
    8, 3
    3, 4
    5, 5
    8, 9
    """
).splitlines()
COORDS = _parse_coordinates(SAMPLE_COORDINATES)
