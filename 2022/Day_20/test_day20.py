from textwrap import dedent

from .aoc_2022_day20 import DECRYPTION_KEY, decrypt, parse_file

SAMPLE_INPUT = dedent(
    """\
    1
    2
    -3
    3
    -2
    0
    4
    """
)
ENCRYPTED = parse_file(SAMPLE_INPUT)


def test_part_one() -> None:
    assert decrypt(ENCRYPTED) == 3


def test_part_two() -> None:
    assert decrypt(ENCRYPTED, decryption_key=DECRYPTION_KEY, n_rounds=10) == 1_623_178_306
