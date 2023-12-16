import pytest

from .aoc_2017_day09 import score_groups

SCORE_TEST_CASES = (
    ("{}", 1),
    ("{{{}}}", 6),
    ("{{},{}}", 5),
    ("{{{},{},{{}}}}", 16),
    ("{<a>,<a>,<a>,<a>}", 1),
    ("{{<ab>},{<ab>},{<ab>},{<ab>}}", 9),
    ("{{<!!>},{<!!>},{<!!>},{<!!>}}", 9),
    ("{{<a!>},{<a!>},{<a!>},{<ab>}}", 3),
)


@pytest.mark.parametrize(("stream", "truth_score"), SCORE_TEST_CASES)
def test_score_groups(stream: str, truth_score: int) -> None:
    assert score_groups(stream)[0] == truth_score


GARBAGE_TEST_CASES = (
    ("<>", 0),
    ("<random characters>", 17),
    ("<<<<>", 3),
    ("<{!>}>", 2),
    ("<!!>", 0),
    ("<!!!>>", 0),
    ("<{o'i!a,<{i<a>", 10),
)


@pytest.mark.parametrize(("stream", "truth_n_garbage"), GARBAGE_TEST_CASES)
def test_count_garbage(stream: str, truth_n_garbage: int) -> None:
    assert score_groups(stream)[1] == truth_n_garbage
