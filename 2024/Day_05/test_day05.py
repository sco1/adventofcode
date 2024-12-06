from textwrap import dedent

import pytest

from .aoc_2024_day05 import (
    PageOrderRule,
    calculate_reordered_sum,
    calculate_valid_sum,
    compile_order_rules,
    is_valid_spec,
    parse_print_spec,
    reorder_spec,
)

PARSING_SAMPLE = dedent(
    """\
    47|53
    97|13

    75,47,61,53,29
    75,29,13
    """
)

TRUTH_RULES = [PageOrderRule(47, 53), PageOrderRule(97, 13)]
TRUTH_UPDATE_SPEC = [[75, 47, 61, 53, 29], [75, 29, 13]]


def test_parse_print_spec() -> None:
    ordering_rules, update_spec = parse_print_spec(PARSING_SAMPLE)
    assert ordering_rules == TRUTH_RULES
    assert update_spec == TRUTH_UPDATE_SPEC


def test_compile_order_rules() -> None:
    order_rules = [
        PageOrderRule(47, 53),
        PageOrderRule(97, 13),
        PageOrderRule(97, 61),
        PageOrderRule(97, 47),
    ]
    truth_compiled = {
        47: {53},
        97: {13, 47, 61},
    }
    truth_reverse_compiled = {
        53: {47},
        13: {97},
        61: {97},
        47: {97},
    }

    assert compile_order_rules(order_rules, reversed=False) == truth_compiled
    assert compile_order_rules(order_rules, reversed=True) == truth_reverse_compiled


SAMPLE_INPUT = dedent(
    """\
    47|53
    97|13
    97|61
    97|47
    75|29
    61|13
    75|53
    29|13
    97|29
    53|29
    61|53
    97|53
    61|29
    47|13
    75|47
    97|75
    47|61
    75|61
    47|29
    75|13
    53|13

    75,47,61,53,29
    97,61,53,29,13
    75,29,13
    75,97,47,61,53
    61,13,29
    97,13,75,29,47
    """
)
SAMPLE_ORDERING_RULES, _ = parse_print_spec(SAMPLE_INPUT)
SAMPLE_COMPILED_RULES = compile_order_rules(SAMPLE_ORDERING_RULES)

SPEC_ORDER_TEST_CASES = (
    ([75, 47, 61, 53, 29], True),
    ([97, 61, 53, 29, 13], True),
    ([75, 29, 13], True),
    ([75, 97, 47, 61, 53], False),
    ([61, 13, 29], False),
    ([97, 13, 75, 29, 47], False),
)


@pytest.mark.parametrize(("spec", "truth_is_valid"), SPEC_ORDER_TEST_CASES)
def test_is_valid(spec: list[int], truth_is_valid: bool) -> None:
    assert is_valid_spec(SAMPLE_COMPILED_RULES, spec) == truth_is_valid


def test_valid_sum() -> None:
    assert calculate_valid_sum(SAMPLE_INPUT) == 143


REORDER_TEST_CASES = (
    ([75, 97, 47, 61, 53], [97, 75, 47, 61, 53]),
    ([61, 13, 29], [61, 29, 13]),
    ([97, 13, 75, 29, 47], [97, 75, 47, 29, 13]),
)


@pytest.mark.parametrize(("spec", "truth_reordered"), REORDER_TEST_CASES)
def test_spec_reorder(spec: list[int], truth_reordered: list[int]) -> None:
    assert reorder_spec(SAMPLE_COMPILED_RULES, spec) == truth_reordered


def test_reorganized_sum() -> None:
    assert calculate_reordered_sum(SAMPLE_INPUT) == 123
