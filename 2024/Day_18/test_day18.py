from textwrap import dedent

from .aoc_2024_day18 import build_grid, find_first_blocker, parse_byte_positions, shortest_path

SAMPLE_INPUT = dedent(
    """\
    5,4
    4,2
    4,5
    3,0
    2,1
    6,3
    2,4
    1,5
    0,6
    3,3
    2,6
    5,1
    1,2
    5,5
    2,5
    6,5
    1,4
    0,4
    6,4
    1,1
    6,1
    1,0
    0,5
    1,6
    2,0
    """
)


def test_shortest_path_len() -> None:
    byte_positions = parse_byte_positions(SAMPLE_INPUT)
    grid = build_grid(byte_positions, dim=7, n_bytes=12)

    assert shortest_path(grid, end=(6, 6)) == 22


def test_find_first_blocker() -> None:
    byte_positions = parse_byte_positions(SAMPLE_INPUT)
    assert find_first_blocker(byte_positions, dim=7, end=(6, 6)) == (6, 1)
