from .aoc_2018_day8 import parse_license_file, sum_tree_metadata

SAMPLE_LICENSE = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"


def test_metadata_sum() -> None:
    tree = parse_license_file(SAMPLE_LICENSE)
    assert sum_tree_metadata(tree) == 138


def test_node_value() -> None:
    tree = parse_license_file(SAMPLE_LICENSE)
    assert tree.value == 66
