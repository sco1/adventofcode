from textwrap import dedent

from .aoc_2022_day03 import is_possible_triangle, parse_triangle_columns


def test_is_triangle() -> None:
    assert is_possible_triangle("5 10 25") is False


VERTICAL_SPEC = dedent(
    """\
    101 301 501
    102 302 502
    103 303 503
    201 401 601
    202 402 602
    203 403 603
    """
)

TRUTH_TRIANGLES = (
    "101 102 103",
    "301 302 303",
    "501 502 503",
    "201 202 203",
    "401 402 403",
    "601 602 603",
)


def test_read_columns() -> None:
    triangles = tuple(parse_triangle_columns(VERTICAL_SPEC))
    assert triangles == TRUTH_TRIANGLES
