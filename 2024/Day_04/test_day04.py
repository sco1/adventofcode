from textwrap import dedent

import pytest

from .aoc_2024_day04 import count_word, count_x_mas, parse_word_search

SAMPLE_INPUT_1 = dedent(
    """\
    ..X...
    .SAMX.
    .A..A.
    XMAS.S
    .X....
    """
)

TRUTH_COORDS_SAMPLE_1 = {
    "X": {(0, 3), (2, 0), (1, 4), (4, 1)},
    "M": {(3, 1), (1, 3)},
    "A": {(2, 3), (1, 2), (2, 1), (4, 2)},
    "S": {(5, 3), (1, 1), (3, 3)},
}


def test_parse_word_search() -> None:
    letter_map, _ = parse_word_search(SAMPLE_INPUT_1)

    # Just check one half, the other is basically just a transformation of the same data
    # For the purposes of AOC this will be fine enough
    assert letter_map == TRUTH_COORDS_SAMPLE_1


SAMPLE_INPUT_2 = dedent(
    """\
    MMMSXXMASM
    MSAMXMSMSA
    AMXSXMAAMM
    MSAMASMSMX
    XMASAMXAMM
    XXAMMXXAMA
    SMSMSASXSS
    SAXAMASAAA
    MAMMMXMMMM
    MXMXAXMASX
    """
)

SAMPLE_INPUT_3 = dedent(
    """\
    ....XXMAS.
    .SAMXMS...
    ...S..A...
    ..A.A.MS.X
    XMASAMX.MM
    X.....XA.A
    S.S.S.S.SS
    .A.A.A.A.A
    ..M.M.M.MM
    .X.X.XMASX
    """
)

COUNTING_TEST_CASES = (
    (SAMPLE_INPUT_1, 4),
    (SAMPLE_INPUT_2, 18),
    (SAMPLE_INPUT_3, 18),
)


@pytest.mark.parametrize(("raw_puzzle", "truth_n"), COUNTING_TEST_CASES)
def test_count_xmas(raw_puzzle: str, truth_n: int) -> None:
    letter_map, letter_coords = parse_word_search(raw_puzzle)
    assert count_word(letter_map, letter_coords) == truth_n


XMAS_SAMPLE = dedent(
    """\
    .M.S......
    ..A..MSMS.
    .M.S.MAA..
    ..A.ASMSM.
    .M.S.M....
    ..........
    S.S.S.S.S.
    .A.A.A.A..
    M.M.M.M.M.
    ..........
    """
)


def test_count_x_mas() -> None:
    letter_map, letter_coords = parse_word_search(XMAS_SAMPLE)
    assert count_x_mas(letter_map, letter_coords) == 9
