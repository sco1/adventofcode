from textwrap import dedent

from .aoc_2018_day3 import (
    _build_cloth,
    _parse_claims,
    calculate_overlap,
    find_nonoverlapping_claim,
)

SAMPLE_CLAIMS = dedent(
    """\
    #1 @ 1,3: 4x4
    #2 @ 3,1: 4x4
    #3 @ 5,5: 2x2
    """
).splitlines()
CLAIMS = _parse_claims(SAMPLE_CLAIMS)
CLOTH = _build_cloth(CLAIMS)


def test_part_one() -> None:
    assert calculate_overlap(CLOTH) == 4


def test_part_two() -> None:
    assert find_nonoverlapping_claim(CLOTH, CLAIMS) == 3
