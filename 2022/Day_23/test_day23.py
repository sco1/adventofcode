from textwrap import dedent

from helpers.parsing import parse_hashed_map
from .aoc_2022_day23 import run_sim, run_until_static

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
    start_coords = parse_hashed_map(SAMPLE_INPUT)
    assert run_sim(start_coords) == 110


def test_part_two() -> None:
    start_coords = parse_hashed_map(SAMPLE_INPUT)
    assert run_until_static(start_coords) == 20
