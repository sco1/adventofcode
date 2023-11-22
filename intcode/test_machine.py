import pytest

from intcode.machine import IntcodeMachine, find_noun_verb

DAY_02_A = (
    ("1,9,10,3,2,3,11,0,99,30,40,50", [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]),
    ("1,0,0,0,99", [2, 0, 0, 0, 99]),
    ("2,3,0,3,99", [2, 3, 0, 6, 99]),
    ("2,4,4,5,99,0", [2, 4, 4, 5, 99, 9801]),
    ("1,1,1,4,99,5,6,0,99", [30, 1, 1, 4, 2, 5, 6, 0, 99]),
)


@pytest.mark.parametrize(("in_program", "truth_end_state"), DAY_02_A)
def test_day_2_out_state(in_program: str, truth_end_state: list[int]) -> None:
    im = IntcodeMachine(in_program)
    im.run()

    assert im._state == truth_end_state


DAY_02_B = [
    ("1,0,0,0,99", 2, (0, 0)),
    ("1,1,1,3,2,3,11,0,99,30,40,50", 3500, (9, 10)),
]


@pytest.mark.parametrize(("in_program", "target_output", "truth_noun_verb"), DAY_02_B)
def test_day_2_find_nv_pair(
    in_program: str, target_output: int, truth_noun_verb: tuple[int, int]
) -> None:
    nv_pair = find_noun_verb(program=in_program, target_output=target_output)
    assert nv_pair == truth_noun_verb
