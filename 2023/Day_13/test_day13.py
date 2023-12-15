from textwrap import dedent

import pytest

from .aoc_2023_day13 import Pattern, find_reflections, parse_patterns, summarize_patterns

SAMPLE_INPUT_EXTENDED = dedent(
    """\
    #.##..##.
    ..#.##.#.
    ##......#
    ##......#
    ..#.##.#.
    ..##..##.
    #.#.##.#.

    #...##..#
    #....#..#
    ..##..###
    #####.##.
    #####.##.
    ..##..###
    #....#..#

    .#.#....#.#.###
    ...#....#...#..
    ....####....#..
    .#.######.#..##
    ###..##..###...
    .#...##...#.###
    ..##....##.....
    .#...##...#..##
    ..##....##..#..
    .##########....
    ##.#.##.#.##...
    ....####.....##
    ##...##...##.##
    ##.#.##.#.##.##
    ...#....#...###
    ##...##...#####
    ....#..........
    """
)
PATTERNS = parse_patterns(SAMPLE_INPUT_EXTENDED)

REFLECTION_TEST_CASES = (  # type: ignore[var-annotated]
    (PATTERNS[0], ([5], [])),
    (PATTERNS[1], ([], [4])),
    (PATTERNS[2], ([14], [])),
)


@pytest.mark.parametrize(("pattern", "truth_reflection"), REFLECTION_TEST_CASES)
def test_find_reflection(pattern: Pattern, truth_reflection: tuple[list[int], list[int]]) -> None:
    assert find_reflections(pattern) == truth_reflection


SAMPLE_INPUT = dedent(
    """\
    #.##..##.
    ..#.##.#.
    ##......#
    ##......#
    ..#.##.#.
    ..##..##.
    #.#.##.#.

    #...##..#
    #....#..#
    ..##..###
    #####.##.
    #####.##.
    ..##..###
    #....#..#
    """
)


def test_summarize() -> None:
    patterns = parse_patterns(SAMPLE_INPUT)
    assert summarize_patterns(patterns) == 405
