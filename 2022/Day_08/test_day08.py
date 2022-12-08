from textwrap import dedent

from .aoc_2022_day08 import count_visible_trees, find_max_scenic_score, parse_tree_map

SAMPLE_INPUT = dedent(
    """\
    30373
    25512
    65332
    33549
    35390
    """
)
TREE_MAP = parse_tree_map(SAMPLE_INPUT)


def test_part_one() -> None:
    assert count_visible_trees(TREE_MAP) == 21


def test_part_two() -> None:
    assert find_max_scenic_score(TREE_MAP) == 8
