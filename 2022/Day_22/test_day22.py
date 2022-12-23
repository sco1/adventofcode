from textwrap import dedent

from .aoc_2022_day22 import find_password, parse_puzzle_input

SAMPLE_INPUT = dedent(
    """\
            ...#
            .#..
            #...
            ....
    ...#.......#
    ........#...
    ..#....#....
    ..........#.
            ...#....
            .....#..
            .#......
            ......#.

    10R5L5R10L4R5L5
    """
)


def test_part_one() -> None:
    floor, walls, bounds, instructions = parse_puzzle_input(SAMPLE_INPUT)
    assert find_password(floor, walls, bounds, instructions) == 6032
