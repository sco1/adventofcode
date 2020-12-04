from textwrap import dedent

import pytest

from .aoc_2020_day03 import TobogganMap


TOBOGGAN_MAP = dedent(
    """\
    ..##.......
    #...#...#..
    .#....#..#.
    ..#.#...#.#
    .#...##..#.
    ..#.##.....
    .#.#.#....#
    .#........#
    #.##...#...
    #...##....#
    .#..#...#.#
    """
)
TOBOGGAN_RUN = TobogganMap(TOBOGGAN_MAP)


STEP_SEQUENCES = [
    ((1, 1), 2),
    ((3, 1), 7),
    ((5, 1), 3),
    ((7, 1), 4),
    ((1, 2), 2),
]


@pytest.mark.parametrize(("step_size", "n_trees_hit"), STEP_SEQUENCES)
def test_toboggan_trajectory(step_size: str, n_trees_hit: int) -> None:
    """Check that the provided step sizes are producing the correct number of trees hit."""
    assert TOBOGGAN_RUN.toboggan_run(step=step_size) == n_trees_hit
