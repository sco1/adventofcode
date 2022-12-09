from textwrap import dedent

import pytest

from .aoc_2022_day09 import parse_instructions, run_sim

SAMPLE_INPUTS = (
    (
        dedent(
            """\
            R 4
            U 4
            L 3
            D 1
            R 4
            D 1
            L 5
            R 2
            """
        ),
        13,
        1,
    ),
    (
        dedent(
            """\
            R 5
            U 8
            L 8
            D 3
            R 17
            D 10
            L 25
            U 20
            """
        ),
        88,
        36,
    ),
)


@pytest.mark.parametrize(("puzzle_input", "truth_seen_pt1", "truth_seen_pt2"), SAMPLE_INPUTS)
def test_part_one(puzzle_input: str, truth_seen_pt1: int, truth_seen_pt2: int) -> None:
    steps = parse_instructions(puzzle_input)
    assert run_sim(steps, 2) == truth_seen_pt1


@pytest.mark.parametrize(("puzzle_input", "truth_seen_pt1", "truth_seen_pt2"), SAMPLE_INPUTS)
def test_part_two(puzzle_input: str, truth_seen_pt1: int, truth_seen_pt2: int) -> None:
    steps = parse_instructions(puzzle_input)
    assert run_sim(steps, 10) == truth_seen_pt2
