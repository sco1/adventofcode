import pytest

from .aoc_2024_day22 import evolve_secret, mix, nth_secret, prune


def test_mix() -> None:
    assert mix(secret=42, val=15) == 37


def test_prune() -> None:
    assert prune(100_000_000) == 16_113_920


def test_evolve_secret() -> None:
    TRUTH_EVOLVE = [
        15_887_950,
        16_495_136,
        527_345,
        704_524,
        1_553_684,
        12_683_156,
        11_100_544,
        12_249_484,
        7_753_432,
        5_908_254,
    ]

    sn = evolve_secret(123)
    secrets = [next(sn) for _ in range(10)]

    assert secrets == TRUTH_EVOLVE


NTH_SECRET_CASES_2000 = (
    (1, 8_685_429),
    (10, 4_700_978),
    (100, 15_273_692),
    (2024, 8_667_524),
)


@pytest.mark.parametrize(("seed", "truth_evolved"), NTH_SECRET_CASES_2000)
def test_nth_secret(seed: int, truth_evolved: int) -> None:
    assert nth_secret(seed, n=2000) == truth_evolved
