from textwrap import dedent

import pytest

from .aoc_2025_day01 import Direction, Rotation, find_password, rotate_dial

INSTRUCTION_TEST_CASES = (
    ("L0", Rotation(Direction.LEFT, 0)),
    ("L69", Rotation(Direction.LEFT, 69)),
    ("R0", Rotation(Direction.RIGHT, 0)),
    ("R69", Rotation(Direction.RIGHT, 69)),
)


@pytest.mark.parametrize(("in_str", "truth_out"), INSTRUCTION_TEST_CASES)
def test_parse_instruction(in_str: str, truth_out: Rotation) -> None:
    assert Rotation.from_str(in_str) == truth_out


ROTATION_TEST_CASES = (
    (11, Rotation(Direction.RIGHT, 8), 19),
    (19, Rotation(Direction.LEFT, 19), 0),
    (0, Rotation(Direction.LEFT, 1), 99),
    (99, Rotation(Direction.RIGHT, 1), 0),
    (5, Rotation(Direction.LEFT, 10), 95),
    (95, Rotation(Direction.RIGHT, 5), 0),
)


@pytest.mark.parametrize(("start", "rotation", "truth_out"), ROTATION_TEST_CASES)
def test_rotate_n(start: int, rotation: Rotation, truth_out: int) -> None:
    assert rotate_dial(start, rotation) == truth_out


SAMPLE_INPUT = dedent(
    """\
    L68
    L30
    R48
    L5
    R60
    L55
    L1
    L99
    R14
    L82
    """
)


def test_find_password() -> None:
    ROTATIONS = [Rotation.from_str(s) for s in SAMPLE_INPUT.splitlines()]
    assert find_password(ROTATIONS) == 3


def test_find_password_secure_method() -> None:
    ROTATIONS = [Rotation.from_str(s) for s in SAMPLE_INPUT.splitlines()]
    assert find_password(ROTATIONS, include_passing=True) == 6
