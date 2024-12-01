from textwrap import dedent

from .aoc_2024_day01 import calculate_similarity_score, calculate_total_distance, split_id_locations

SAMPLE_INPUT = (
    dedent(
        """\
    3   4
    4   3
    2   5
    1   3
    3   9
    3   3
    """
    )
    .strip()
    .splitlines()
)


def test_split_id_locations() -> None:
    truth_left = [1, 2, 3, 3, 3, 4]
    truth_right = [3, 3, 3, 4, 5, 9]

    assert split_id_locations(SAMPLE_INPUT) == (truth_left, truth_right)


def test_calculate_total_distance() -> None:
    left_group, right_group = split_id_locations(SAMPLE_INPUT)
    assert calculate_total_distance(left_group, right_group) == 11


def test_calculate_similarity_score() -> None:
    left_group, right_group = split_id_locations(SAMPLE_INPUT)
    assert calculate_similarity_score(left_group, right_group) == 31
