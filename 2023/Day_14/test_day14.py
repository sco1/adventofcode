from textwrap import dedent

from .aoc_2023_day14 import PlatformMap, TiltDirection

SAMPLE_INPUT = dedent(
    """\
    O....#....
    O.OO#....#
    .....##...
    OO.#O....O
    .O.....O#.
    O.#..O.#.#
    ..O..#O..O
    .......O..
    #....###..
    #OO..#....
    """
)


def test_support_load() -> None:
    plat = PlatformMap.from_raw(SAMPLE_INPUT)
    plat.tilt(TiltDirection.NORTH)

    assert plat.support_load == 136


def test_spin_cycle() -> None:
    plat = PlatformMap.from_raw(SAMPLE_INPUT)
    plat.spin_cycle()

    assert plat.support_load == 64
