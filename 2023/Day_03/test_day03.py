from textwrap import dedent

from .aoc_2023_day03 import find_adjacent_parts, find_gears, parse_schematic, sum_gear_ratios

SAMPLE_INPUT = dedent(
    """\
    467..114..
    ...*......
    ..35..633.
    ......#...
    617*......
    .....+.58.
    ..592.....
    ......755.
    ...$.*....
    .664.598..
    """
)
TRUTH_N_SYMBOLS = sum(1 for c in SAMPLE_INPUT if c in {"*", "#", "+", "$"})


def test_schematic_parsing() -> None:
    nums, symbol_locs = parse_schematic(SAMPLE_INPUT)
    assert len(nums) == 10
    assert len(symbol_locs) == TRUTH_N_SYMBOLS


def test_adjacent_parts() -> None:
    emitted = list(find_adjacent_parts(*parse_schematic(SAMPLE_INPUT)))
    emitted_set = set(emitted)

    assert sum(emitted) == 4361
    assert not (emitted_set & {141, 58})  # 114 and 58 aren't valid part numbers


SAMPLE_ADJACENT = dedent(
    """\
    467..114..
    ...*......
    467..123..
    """
)


def test_multiple_part_instances() -> None:
    emitted = list(find_adjacent_parts(*parse_schematic(SAMPLE_ADJACENT)))
    assert len(emitted) == 2
    assert sum(emitted) == (467 * 2)


def test_find_gears() -> None:
    emitted = list(find_gears(*parse_schematic(SAMPLE_INPUT)))
    assert len(emitted) == 2


def test_gear_ratio_sum() -> None:
    val = sum_gear_ratios(find_gears(*parse_schematic(SAMPLE_INPUT)))
    assert val == 467_835
