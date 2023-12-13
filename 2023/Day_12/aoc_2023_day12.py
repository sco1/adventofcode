import itertools
from collections import abc
from dataclasses import dataclass
from enum import StrEnum
from functools import cached_property
from pathlib import Path


class SpringState(StrEnum):  # noqa: D101
    DAMAGED = "#"
    OPERATIONAL = "."
    UNKNOWN = "?"


@dataclass
class ConditionRecord:  # noqa: D101
    condition: tuple[SpringState]
    pattern: list[int]

    @cached_property
    def _condition_string(self) -> str:
        return "".join(self.condition)


def parse_condition_record(condition_record: str, unfold: bool = False) -> ConditionRecord:
    """
    Parse the provided spring condition record into its respective `ConditionRecord` representation.

    Raw records are assumed to be provided of the form `<spring conditions> <spring groups>`, where
    spring condition is mapped by its status: operational (`.`), damaged (`#`), or unknown (`?`).
    Following the spring condition string is a comma separated list of integers, specifying the
    sizes of each contiguous group of damaged springs.

    For example, `#.#.### 1,1,3` describes a spring record with no unknown conditions.

    If `unfold` is `True`, the record is unfolded 5 times, where the condition record is delimited
    by `?`, e.g. `.# 1` would become `.#?.#?.#?.#?.# 1,1,1,1,1`.
    """
    raw_conditions, raw_pattern = condition_record.split()

    if unfold:
        raw_conditions = "?".join(raw_conditions for _ in range(5))
        raw_pattern = ",".join(raw_pattern for _ in range(5))

    conditions = tuple(SpringState(c) for c in raw_conditions)
    pattern = [int(v) for v in raw_pattern.split(",")]

    return ConditionRecord(conditions, pattern)


def count_spring_groups(spring_condition: abc.Iterable[SpringState]) -> list[int]:
    """
    Summarize the group sizes of continuous groups of damaged springs in the provided collection.

    For example, the representation of `.#.###.#.######` would return `[1, 3, 1, 6]`.

    NOTE: It is assumed that the provided collection does not contain any unknown conditions (`?`).
    """
    group_sizes = []
    g_len = 0
    for c in spring_condition:
        if c == SpringState.DAMAGED:
            g_len += 1
        else:
            if g_len != 0:
                group_sizes.append(g_len)
                g_len = 0
    else:
        # Catch grouping if it's at the end of the string
        if g_len != 0:
            group_sizes.append(g_len)

    return group_sizes


def count_valid_substitutions(spring_condition: ConditionRecord) -> int:
    """
    Determine the number of valid combinations of spring states satisfy the reported pattern.

    e.g. `???.### 1,1,3` has one valid substitution: `#.#.###`

    NOTE: This is a brute-force solution and does not scale well!
    """
    n_valid = 0
    unknown_idx = [
        idx
        for idx, state in enumerate(spring_condition.condition)
        if (state == SpringState.UNKNOWN)
    ]
    for subs in itertools.product(".#", repeat=len(unknown_idx)):
        query_state = [*spring_condition.condition]  # Copy original
        for idx, sub in zip(unknown_idx, subs):
            query_state[idx] = SpringState(sub)

        if count_spring_groups(query_state) == spring_condition.pattern:
            n_valid += 1

    return n_valid


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    records = [parse_condition_record(line) for line in puzzle_input.splitlines()]
    print(f"Part One: {sum(count_valid_substitutions(r) for r in records)}")

    records = [parse_condition_record(line, unfold=True) for line in puzzle_input.splitlines()]
    print(f"Part Two: {sum(count_valid_substitutions(r) for r in records)}")
