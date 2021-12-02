from textwrap import dedent

from .aoc_2021_day02 import SubMcSubFace

SAMPLE_INPUT = dedent(
    """\
    forward 5
    down 5
    forward 8
    up 3
    down 8
    forward 2
    """
).splitlines()


def test_part_one() -> None:
    toot_toot = SubMcSubFace(SAMPLE_INPUT)
    toot_toot.run()

    assert (toot_toot.horizontal * toot_toot.depth) == 150


def test_part_two() -> None:
    toot_toot = SubMcSubFace(SAMPLE_INPUT, is_aiming=True)
    toot_toot.run()

    assert (toot_toot.horizontal * toot_toot.depth) == 900
