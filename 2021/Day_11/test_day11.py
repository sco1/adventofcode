from textwrap import dedent

from .aoc_2021_day11 import find_first_sync, model_dumbo_cave, parse_energy_levels

SAMPLE_INPUT = dedent(
    """\
    5483143223
    2745854711
    5264556173
    6141336146
    6357385478
    4167524645
    2176841721
    6882881134
    4846848554
    5283751526
    """
).splitlines()


def test_part_one() -> None:
    starting_energy = parse_energy_levels(SAMPLE_INPUT)  # reparse since we mutate in place
    assert model_dumbo_cave(starting_energy, 100) == 1656


def test_part_two() -> None:
    starting_energy = parse_energy_levels(SAMPLE_INPUT)  # reparse since we mutate in place
    assert find_first_sync(starting_energy) == 195
