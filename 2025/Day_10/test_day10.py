import pytest

from .aoc_2025_day10 import MachineSpec, best_button_press

MACHINE_SPEC_TEST_CASES = (
    (
        "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}",
        MachineSpec(
            [False, True, True, False],
            [[3], [1, 3], [2], [2, 3], [0, 2], [0, 1]],
            [3, 5, 4, 7],
            4,
            6,
            4,
        ),
    ),
    (
        "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}",
        MachineSpec(
            [False, False, False, True, False],
            [[0, 2, 3, 4], [2, 3], [0, 4], [0, 1, 2], [1, 2, 3, 4]],
            [7, 5, 12, 7, 2],
            5,
            5,
            5,
        ),
    ),
    (
        "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}",
        MachineSpec(
            [False, True, True, True, False, True],
            [[0, 1, 2, 3, 4], [0, 3, 4], [0, 1, 2, 4, 5], [1, 2]],
            [10, 11, 11, 5, 10, 5],
            6,
            4,
            6,
        ),
    ),
)


@pytest.mark.parametrize(("raw_spec", "truth_out"), MACHINE_SPEC_TEST_CASES)
def test_spec_parse(raw_spec: str, truth_out: MachineSpec) -> None:
    assert MachineSpec.from_raw(raw_spec) == truth_out


BEST_PRESS_TEST_CASES = (
    ("[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}", 2),
    ("[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}", 3),
    ("[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}", 2),
)


@pytest.mark.parametrize(("raw_spec", "truth_out"), BEST_PRESS_TEST_CASES)
def test_best_button_press(raw_spec: str, truth_out: int) -> None:
    spec = MachineSpec.from_raw(raw_spec)
    assert best_button_press(spec) == truth_out
