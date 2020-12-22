from textwrap import dedent

from .aoc_2020_day17 import ConwayCube


STARTING_SLICE = dedent(
    """\
    .#.
    ..#
    ###
    """
)


def test_part_one() -> None:  # noqa: D103
    cube = ConwayCube(STARTING_SLICE)
    cube.step_n(6)

    assert cube.n_active == 112


def test_part_two() -> None:  # noqa: D103
    cube = ConwayCube(STARTING_SLICE, ndims=4)
    cube.step_n(6)

    assert cube.n_active == 848
