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


# Program, input, truth_output
LONG_PROGRAM = "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"
DAY_05_B = [
    # Input equal to 8, position mode
    ("3,9,8,9,10,9,4,9,99,-1,8", ("-1",), "0"),
    ("3,9,8,9,10,9,4,9,99,-1,8", ("0",), "0"),
    ("3,9,8,9,10,9,4,9,99,-1,8", ("8",), "1"),
    ("3,9,8,9,10,9,4,9,99,-1,8", ("9",), "0"),
    # Input less than 8, position mode
    ("3,9,7,9,10,9,4,9,99,-1,8", ("-1",), "1"),
    ("3,9,7,9,10,9,4,9,99,-1,8", ("0",), "1"),
    ("3,9,7,9,10,9,4,9,99,-1,8", ("8",), "0"),
    ("3,9,7,9,10,9,4,9,99,-1,8", ("9",), "0"),
    # Input equal to 8, immediate mode
    ("3,3,1108,-1,8,3,4,3,99", ("-1",), "0"),
    ("3,3,1108,-1,8,3,4,3,99", ("0",), "0"),
    ("3,3,1108,-1,8,3,4,3,99", ("8",), "1"),
    ("3,3,1108,-1,8,3,4,3,99", ("9",), "0"),
    # Input less than 8, immediate mode
    ("3,3,1107,-1,8,3,4,3,99", ("-1",), "1"),
    ("3,3,1107,-1,8,3,4,3,99", ("0",), "1"),
    ("3,3,1107,-1,8,3,4,3,99", ("8",), "0"),
    ("3,3,1107,-1,8,3,4,3,99", ("9",), "0"),
    # Jump test, 0 if input is 0, 1 otherwise, position mode
    ("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9", ("-1",), "1"),
    ("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9", ("0",), "0"),
    ("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9", ("1",), "1"),
    # Jump test, 0 if input is 0, 1 otherwise, immediate mode
    ("3,3,1105,-1,9,1101,0,0,12,4,12,99,1", ("-1",), "1"),
    ("3,3,1105,-1,9,1101,0,0,12,4,12,99,1", ("0",), "0"),
    ("3,3,1105,-1,9,1101,0,0,12,4,12,99,1", ("1",), "1"),
    # Output 999 if input is below 8, 1000 if equal to 8, 1001 if greater than 8
    (LONG_PROGRAM, ("-1",), "999"),
    (LONG_PROGRAM, ("0",), "999"),
    (LONG_PROGRAM, ("8",), "1000"),
    (LONG_PROGRAM, ("9",), "1001"),
]


@pytest.mark.parametrize(("program", "user_input", "truth_output"), DAY_05_B)
def test_day_5_opcodes(program: str, user_input: str, truth_output: str) -> None:
    im = IntcodeMachine(program, user_input)
    im.run()
    assert im.stdout[0] == truth_output
