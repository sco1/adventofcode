from .AoC2017_Day6 import reallocate_banks

BANKS = (0, 2, 7, 0)


def test_part_one() -> None:
    n_steps, _ = reallocate_banks(list(BANKS))
    assert n_steps == 5


def test_part_two() -> None:
    _, loop_size = reallocate_banks(list(BANKS))
    assert loop_size == 4
