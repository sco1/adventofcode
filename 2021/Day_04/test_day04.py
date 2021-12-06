from textwrap import dedent

from .aoc_2021_day04 import parse_bingo, run_bingo

SAMPLE_INPUT = dedent(
    """\
    7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

    22 13 17 11  0
     8  2 23  4 24
    21  9 14 16  7
     6 10  3 18  5
     1 12 20 15 19

     3 15  0  2 22
     9 18 13 17  5
    19  8  7 25 23
    20 11 10 24  4
    14 21 16 12  6

    14 21 17 24  4
    10 16 15  9 19
    18  8 23 26 20
    22 11 13  6  5
     2  0 12  3  7
    """
).splitlines()


def test_part_one() -> None:
    nums, boards = parse_bingo(SAMPLE_INPUT)
    winning_scores = list(run_bingo(nums, boards))
    assert winning_scores[0] == 4512


def test_part_two() -> None:
    nums, boards = parse_bingo(SAMPLE_INPUT)
    winning_scores = list(run_bingo(nums, boards))
    print(winning_scores)
    assert winning_scores[-1] == 1924
