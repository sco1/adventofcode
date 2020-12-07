import typing as t
from textwrap import dedent

import pytest

from .aoc_2020_day07 import build_bag_graph, n_contained_bags, n_valid_bags


class BagTestCase(t.NamedTuple):
    """Helper container for luggage processing test cases."""

    rule_input: str
    n_containing_shinygold: int  # Part One
    n_sub_bags: int  # Part Two


BAG_TEST_CASES = [
    BagTestCase(
        dedent(
            """\
            light red bags contain 1 bright white bag, 2 muted yellow bags.
            dark orange bags contain 3 bright white bags, 4 muted yellow bags.
            bright white bags contain 1 shiny gold bag.
            muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
            shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
            dark olive bags contain 3 faded blue bags, 4 dotted black bags.
            vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
            faded blue bags contain no other bags.
            dotted black bags contain no other bags.
            """
        ),
        4,
        32,
    ),
    BagTestCase(
        dedent(
            """\
            shiny gold bags contain 2 dark red bags.
            dark red bags contain 2 dark orange bags.
            dark orange bags contain 2 dark yellow bags.
            dark yellow bags contain 2 dark green bags.
            dark green bags contain 2 dark blue bags.
            dark blue bags contain 2 dark violet bags.
            dark violet bags contain no other bags.
            """
        ),
        0,
        126,
    ),
]


@pytest.mark.parametrize(("rule_input", "n_containing_shinygold", "n_sub_bags"), BAG_TEST_CASES)
def test_luggage_processing(rule_input: str, n_containing_shinygold: int, n_sub_bags: int) -> None:
    """Check for correct processing of the provided luggage rule sets."""
    rule_graph = build_bag_graph(rule_input.splitlines())
    assert n_valid_bags(rule_graph, "shiny gold") == n_containing_shinygold
    assert n_contained_bags(rule_graph) == n_sub_bags
