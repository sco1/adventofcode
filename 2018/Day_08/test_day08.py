from .aoc_2018_day8 import build_license_tree, root_node_value, sum_metadata

SAMPLE_LICENSE = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"


def test_part_one() -> None:
    tree = build_license_tree(SAMPLE_LICENSE)
    assert sum_metadata(tree) == 138


def test_part_two() -> None:
    tree = build_license_tree(SAMPLE_LICENSE)
    assert root_node_value(tree) == 66
