import pytest

from .aoc_2022_day17 import sim_n_pieces

SAMPLE_INPUT = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"


def test_part_one() -> None:
    assert sim_n_pieces(SAMPLE_INPUT, n_pieces=2_022) == 3068


@pytest.mark.skip(reason="Not brute force friendly")
def test_part_two() -> None:
    assert sim_n_pieces(SAMPLE_INPUT, n_pieces=1_000_000_000_000) == 1_514_285_714_288
