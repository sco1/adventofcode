from textwrap import dedent

import pytest

from .aoc_2021_day18 import (
    PAIR,
    _explode_pair,
    _split_number,
    calculate_magnitude,
    calculate_sum,
    largest_magnitude,
)

EXPLODE_TESTS = [
    ("[[[[[9,8],1],2],3],4]", "[[[[0,9],2],3],4]"),
    ("[7,[6,[5,[4,[3,2]]]]]", "[7,[6,[5,[7,0]]]]"),
    ("[[6,[5,[4,[3,2]]]],1]", "[[6,[5,[7,0]]],3]"),
    ("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"),
]


@pytest.mark.parametrize(("snailfish_number", "truth_exploded"), EXPLODE_TESTS)
def test_snailfish_number_explode(snailfish_number: str, truth_exploded: str) -> None:
    # These test cases will all explode the first pair
    to_explode = PAIR.search(snailfish_number)
    assert _explode_pair(snailfish_number, to_explode) == truth_exploded


SPLIT_TESTS = [
    ("10", "[5,5]"),
    ("11", "[5,6]"),
    ("12", "[6,6]"),
]


@pytest.mark.parametrize(("regular_number", "truth_split"), SPLIT_TESTS)
def test_snailfish_number_split(regular_number: str, truth_split: str) -> None:
    assert _split_number(regular_number) == truth_split


MAGNITUDE_TESTS = [
    ("[[1,2],[[3,4],5]]", 143),
    ("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", 1384),
    ("[[[[1,1],[2,2]],[3,3]],[4,4]]", 445),
    ("[[[[3,0],[5,3]],[4,4]],[5,5]]", 791),
    ("[[[[5,0],[7,4]],[5,5]],[6,6]]", 1137),
    ("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]", 3488),
]


@pytest.mark.parametrize(("snailfish_number", "truth_magnitude"), MAGNITUDE_TESTS)
def test_snailfish_magnitude(snailfish_number: str, truth_magnitude: int) -> None:
    assert calculate_magnitude(snailfish_number) == truth_magnitude


SUMMATION_TESTS = [
    (
        dedent(
            """\
            [[[[4,3],4],4],[7,[[8,4],9]]]
            [1,1]
            """
        ).splitlines(),
        "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]",
    ),
    (
        dedent(
            """\
            [1,1]
            [2,2]
            [3,3]
            [4,4]
            """
        ).splitlines(),
        "[[[[1,1],[2,2]],[3,3]],[4,4]]",
    ),
    (
        dedent(
            """\
            [1,1]
            [2,2]
            [3,3]
            [4,4]
            [5,5]
            """
        ).splitlines(),
        "[[[[3,0],[5,3]],[4,4]],[5,5]]",
    ),
    (
        dedent(
            """\
            [1,1]
            [2,2]
            [3,3]
            [4,4]
            [5,5]
            [6,6]
            """
        ).splitlines(),
        "[[[[5,0],[7,4]],[5,5]],[6,6]]",
    ),
    (
        dedent(
            """\
            [[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
            [7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
            [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
            [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
            [7,[5,[[3,8],[1,4]]]]
            [[2,[2,2]],[8,[8,1]]]
            [2,9]
            [1,[[[9,3],9],[[9,0],[0,7]]]]
            [[[5,[7,4]],7],1]
            [[[[4,2],2],6],[8,7]]
            """
        ).splitlines(),
        "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]",
    ),
    (
        dedent(
            """\
            [[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
            [[[5,[2,8]],4],[5,[[9,9],0]]]
            [6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
            [[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
            [[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
            [[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
            [[[[5,4],[7,7]],8],[[8,3],8]]
            [[9,3],[[9,9],[6,[4,9]]]]
            [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
            [[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
            """
        ).splitlines(),
        "[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]",
    ),
]


@pytest.mark.parametrize(("snailfish_numbers", "truth_sum"), SUMMATION_TESTS)
def test_summation(snailfish_numbers: list[str], truth_sum: str) -> None:
    assert calculate_sum(snailfish_numbers) == truth_sum


SAMPLE_HOMEWORK = dedent(
    """\
    [[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
    [[[5,[2,8]],4],[5,[[9,9],0]]]
    [6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
    [[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
    [[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
    [[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
    [[[[5,4],[7,7]],8],[[8,3],8]]
    [[9,3],[[9,9],[6,[4,9]]]]
    [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
    [[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
    """
).splitlines()


def test_part_one() -> None:
    final_sum = calculate_sum(SAMPLE_HOMEWORK)
    assert calculate_magnitude(final_sum) == 4140


def test_part_two() -> None:
    assert largest_magnitude(SAMPLE_HOMEWORK) == 3993
