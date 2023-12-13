import pytest

from .aoc_2023_day12 import (
    ConditionRecord,
    SpringState,
    count_valid_substitutions,
    parse_condition_record,
)


def test_condition_parsing() -> None:
    spring_spec = "???.### 1,1,3"
    truth_condition = (
        SpringState.UNKNOWN,
        SpringState.UNKNOWN,
        SpringState.UNKNOWN,
        SpringState.OPERATIONAL,
        SpringState.DAMAGED,
        SpringState.DAMAGED,
        SpringState.DAMAGED,
    )
    truth_pattern = [1, 1, 3]
    truth_record = ConditionRecord(truth_condition, truth_pattern)

    assert parse_condition_record(spring_spec) == truth_record


COMBINATIONS_TEST_CASES = (
    ("???.### 1,1,3", 1),
    (".??..??...?##. 1,1,3", 4),
    ("?#?#?#?#?#?#?#? 1,3,1,6", 1),
    ("????.#...#... 4,1,1", 1),
    ("????.######..#####. 1,6,5", 4),
    ("?###???????? 3,2,1", 10),
)


@pytest.mark.parametrize(("spring_spec", "truth_n_combos"), COMBINATIONS_TEST_CASES)
def test_n_combinations(spring_spec: str, truth_n_combos: int) -> None:
    record = parse_condition_record(spring_spec)
    assert count_valid_substitutions(record) == truth_n_combos


UNFOLD_PARSING_TEST_CASES = (
    (".# 1", ".#?.#?.#?.#?.# 1,1,1,1,1"),
    ("???.### 1,1,3", "???.###????.###????.###????.###????.### 1,1,3,1,1,3,1,1,3,1,1,3,1,1,3"),
)


@pytest.mark.parametrize(("folded_spec", "truth_unfolded"), UNFOLD_PARSING_TEST_CASES)
def test_unfold_parsing(folded_spec: str, truth_unfolded: str) -> None:
    unfolded = parse_condition_record(folded_spec, unfold=True)
    assert unfolded == parse_condition_record(truth_unfolded)


UNFOLDING_TEST_CASES = (
    ("???.### 1,1,3", 1),
    (".??..??...?##. 1,1,3", 16_384),
    ("?#?#?#?#?#?#?#? 1,3,1,6", 1),
    ("????.#...#... 4,1,1", 16),
    ("????.######..#####. 1,6,5", 2500),
    ("?###???????? 3,2,1", 506_250),
)


@pytest.mark.skip(reason="Not brute force friendly")
@pytest.mark.parametrize(("spring_spec", "truth_n_combos"), UNFOLDING_TEST_CASES)
def test_n_combinations_unfolded(spring_spec: str, truth_n_combos: int) -> None:
    record = parse_condition_record(spring_spec, unfold=True)
    assert count_valid_substitutions(record) == truth_n_combos
