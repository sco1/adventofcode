from textwrap import dedent

import pytest

from .aoc_2022_day13 import calc_decoder_key, calc_valid_sum, check_order, parse_packets

COMPARISON_CASES = (  # type: ignore[var-annotated]
    ([1, 1, 3, 1, 1], [1, 1, 5, 1, 1], True),
    ([[1], [2, 3, 4]], [[1], 4], True),
    ([9], [[8, 7, 6]], False),
    ([[4, 4], 4, 4], [[4, 4], 4, 4, 4], True),
    ([7, 7, 7, 7], [7, 7, 7], False),
    ([], [3], True),
    ([[[]]], [[]], False),
    ([1, [2, [3, [4, [5, 6, 7]]]], 8, 9], [1, [2, [3, [4, [5, 6, 0]]]], 8, 9], False),
    (
        [
            [0, 6, [3, 1, [2], [8, 6, 3, 8, 1], 6]],
            [6, [[3], [7, 6, 4, 9], 8, [6, 4, 8, 8, 1], 7]],
            [],
        ],
        [
            [[[10, 0], 4]],
            [],
            [7, [[8], 1], [[3, 3, 10, 9, 4], [0, 8, 2, 0, 5], [], [2, 3, 3, 4, 4]], 10, 6],
            [[], [[5, 7, 1], 10], [[1, 3, 3], [10, 9], [6, 3, 10], 5]],
        ],
        True,
    ),
)


@pytest.mark.parametrize(("left", "right", "truth_comp"), COMPARISON_CASES)
def test_comparisons(left: list, right: list, truth_comp: bool) -> None:
    assert (check_order(left, right) < 0) == truth_comp


SAMPLE_INPUT = dedent(
    """\
    [1,1,3,1,1]
    [1,1,5,1,1]

    [[1],[2,3,4]]
    [[1],4]

    [9]
    [[8,7,6]]

    [[4,4],4,4]
    [[4,4],4,4,4]

    [7,7,7,7]
    [7,7,7]

    []
    [3]

    [[[]]]
    [[]]

    [1,[2,[3,[4,[5,6,7]]]],8,9]
    [1,[2,[3,[4,[5,6,0]]]],8,9]
    """
)


def test_part_one() -> None:
    assert calc_valid_sum(parse_packets(SAMPLE_INPUT)) == 13


def test_part_two() -> None:
    assert calc_decoder_key(parse_packets(SAMPLE_INPUT, insert_divider=True)) == 140
