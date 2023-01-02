from textwrap import dedent

from .aoc_2022_day23 import parse_scan, run_sim, run_until_static

SAMPLE_INPUT = dedent(
    """\
    ....#..
    ..###.#
    #...#.#
    .#...##
    #.###..
    ##.#.##
    .#..#..
    """
)


def test_part_one() -> None:
    start_coords = parse_scan(SAMPLE_INPUT)
    assert run_sim(start_coords) == 110


def test_part_two() -> None:
    start_coords = parse_scan(SAMPLE_INPUT)
    assert run_until_static(start_coords) == 20
