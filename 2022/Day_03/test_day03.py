from textwrap import dedent

import pytest

from .aoc_2022_day03 import calculate_overlap_priority, score_groups, score_rucksacks

SAMPLE_RUCKSACKS = (
    ("vJrwpWtwJgWrhcsFMMfFFhFp", 16),
    ("jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL", 38),
    ("PmmdzqPrVvPwwTWBwg", 42),
    ("wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn", 22),
    ("ttgJtRGJQctTZtZT", 20),
    ("CrZsJsPPZsGzwwsLwLmpwMDw", 19),
)


@pytest.mark.parametrize(("rucksack", "truth_priority"), SAMPLE_RUCKSACKS)
def test_rucksack_check(rucksack: str, truth_priority: int) -> None:
    priority = calculate_overlap_priority(rucksack)
    assert priority == truth_priority


SAMPLE_CONTENTS = dedent(
    """\
    vJrwpWtwJgWrhcsFMMfFFhFp
    jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
    PmmdzqPrVvPwwTWBwg
    wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
    ttgJtRGJQctTZtZT
    CrZsJsPPZsGzwwsLwLmpwMDw
    """
)


def test_priority_check() -> None:
    assert score_rucksacks(SAMPLE_CONTENTS.splitlines()) == 157


SAMPLE_GROUPS = (
    (
        dedent(
            """\
            vJrwpWtwJgWrhcsFMMfFFhFp
            jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
            PmmdzqPrVvPwwTWBwg
            """
        ),
        18,
    ),
    (
        dedent(
            """\
            wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
            ttgJtRGJQctTZtZT
            CrZsJsPPZsGzwwsLwLmpwMDw
            """
        ),
        52,
    ),
    (
        dedent(
            """\
            vJrwpWtwJgWrhcsFMMfFFhFp
            jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
            PmmdzqPrVvPwwTWBwg
            wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
            ttgJtRGJQctTZtZT
            CrZsJsPPZsGzwwsLwLmpwMDw
            """
        ),
        70,
    ),
)


@pytest.mark.parametrize(("group", "truth_score"), SAMPLE_GROUPS)
def test_group_rucksack_check(group: str, truth_score: int) -> None:
    assert score_groups(group.splitlines()) == truth_score
