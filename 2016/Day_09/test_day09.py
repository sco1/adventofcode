import pytest

from .aoc_2016_day09 import decompress

TEST_CASES = (
    ("ADVENT", "ADVENT"),
    ("A(1x5)BC", "ABBBBBC"),
    ("(3x3)XYZ", "XYZXYZXYZ"),
    ("A(2x2)BCD(2x2)EFG", "ABCBCDEFEFG"),
    ("(6x1)(1x3)A", "(1x3)A"),
    ("X(8x2)(3x3)ABCY", "X(3x3)ABC(3x3)ABCY"),
)


@pytest.mark.parametrize(("compressed", "truth_decompressed"), TEST_CASES)
def test_decryption(compressed: str, truth_decompressed: str) -> None:
    assert decompress(compressed) == truth_decompressed


V2_TEST_CASES = (
    ("(3x3)XYZ", "XYZXYZXYZ"),
    ("X(8x2)(3x3)ABCY", "XABCABCABCABCABCABCY"),
    ("(27x12)(20x12)(13x14)(7x10)(1x12)A", "A" * 241_920),
)


@pytest.mark.parametrize(
    ("compressed", "truth_decompressed"),
    V2_TEST_CASES,
    ids=lambda s: f"{s[:10]} ...",  # Pytest doesn't like the 240k character parameter
)
def test_v2_decryption(compressed: str, truth_decompressed: str) -> None:
    assert decompress(compressed, recurse=True) == truth_decompressed


def test_v2_decryption_len() -> None:
    file = "(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN"
    assert len(decompress(file, recurse=True)) == 445
