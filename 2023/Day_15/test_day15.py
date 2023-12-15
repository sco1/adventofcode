import pytest

from .aoc_2023_day15 import bin_lenses, calculate_focusing_power, hash_val

SAMPLE_HASH_STEPS = (
    ("HASH", 52),
    ("rn=1", 30),
    ("cm-", 253),
    ("qp=3", 97),
    ("cm=2", 47),
    ("qp-", 14),
    ("pc=4", 180),
    ("ot=9", 9),
    ("ab=5", 197),
    ("pc-", 48),
    ("pc=6", 214),
    ("ot=7", 231),
)


@pytest.mark.parametrize(("hash", "truth_val"), SAMPLE_HASH_STEPS)
def test_hash_value(hash: str, truth_val: int) -> None:
    assert hash_val(hash) == truth_val


SAMPLE_INPUT = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"


def test_full_hash_decode() -> None:
    assert sum(hash_val(h) for h in SAMPLE_INPUT.split(",")) == 1320


def test_focusing_power() -> None:
    boxes = bin_lenses(SAMPLE_INPUT)
    assert calculate_focusing_power(boxes) == 145
