import math
from collections import abc

from .aoc_2025_day06 import execute_worksheet, parse_worksheet

SAMPLE_INPUT = """\
123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +
"""
TRUTH_COLS = [
    [123, 45, 6],
    [328, 64, 98],
    [51, 387, 215],
    [64, 23, 314],
]
TRUTH_OPERATORS: list[abc.Callable] = [math.prod, sum, math.prod, sum]
TRUTH_TOTAL = 4_277_556

TRUTH_CEPH_COLS = [
    [4, 431, 623],
    [175, 581, 32],
    [8, 248, 369],
    [356, 24, 1],
]
TRUTH_CEPH_OPERATORS: list[abc.Callable] = [sum, math.prod, sum, math.prod]
TRUTH_CEPH_TOTAL = 3_263_827


def test_parse_worksheet() -> None:
    cols, operators = parse_worksheet(SAMPLE_INPUT)
    assert cols == TRUTH_COLS
    assert operators == TRUTH_OPERATORS


def test_parse_worksheet_cephalopod() -> None:
    cols, operators = parse_worksheet(SAMPLE_INPUT, cephalopod=True)
    assert cols == TRUTH_CEPH_COLS
    assert operators == TRUTH_CEPH_OPERATORS


def test_worksheet_exec() -> None:
    assert execute_worksheet(TRUTH_COLS, TRUTH_OPERATORS) == TRUTH_TOTAL
    assert execute_worksheet(TRUTH_CEPH_COLS, TRUTH_CEPH_OPERATORS) == TRUTH_CEPH_TOTAL
