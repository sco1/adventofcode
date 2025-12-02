import pytest

from .aoc_2025_day02 import ProductIDRange, find_invalid_ids, invalid_id_sum, is_valid_id

PRODUCT_PARSE_CASES = (
    ("11-22", ProductIDRange(11, 22)),
    ("95-115", ProductIDRange(95, 115)),
    ("998-1012", ProductIDRange(998, 1012)),
)


@pytest.mark.parametrize(("raw_id", "truth_out"), PRODUCT_PARSE_CASES)
def test_product_id_parse(raw_id: str, truth_out: ProductIDRange) -> None:
    assert ProductIDRange.from_raw(raw_id) == truth_out


ID_VALID_CASES = (
    (11, False),
    (22, False),
    (1010, False),
    (1188511885, False),
    (222222, False),
    (446446, False),
    (38593859, False),
    (12, True),
    (999, True),
    (101, True),
    (1011, True),
)


@pytest.mark.parametrize(("product_id", "truth_out"), ID_VALID_CASES)
def test_is_valid_id(product_id: int, truth_out: bool) -> None:
    assert is_valid_id(product_id) == truth_out


ID_RANGE_TEST_CASES: tuple[tuple[ProductIDRange, list[int]], ...] = (
    (ProductIDRange(11, 22), [11, 22]),
    (ProductIDRange(95, 115), [99]),
    (ProductIDRange(998, 1012), [1010]),
    (ProductIDRange(1_188_511_880, 1_188_511_890), [1_188_511_885]),
    (ProductIDRange(222_220, 222_224), [222_222]),
    (ProductIDRange(446_443, 446_449), [446_446]),
    (ProductIDRange(38_593_856, 38_593_862), [38_593_859]),
    (ProductIDRange(1_698_522, 1_698_528), []),
    (ProductIDRange(565_653, 565_659), []),
    (ProductIDRange(824_824_821, 824_824_827), []),
    (ProductIDRange(2_121_212_118, 2_121_212_124), []),
)


@pytest.mark.parametrize(("id_range", "truth_out"), ID_RANGE_TEST_CASES)
def test_find_invalid_ids(id_range: ProductIDRange, truth_out: list[int]) -> None:
    assert find_invalid_ids(id_range) == truth_out


def test_invalid_id_sum() -> None:
    ID_COLLECTION = [[1], [2, 3], []]
    assert invalid_id_sum(ID_COLLECTION) == 6


SAMPLE_INPUT = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"
SAMPLE_ID_RANGES = [ProductIDRange.from_raw(s) for s in SAMPLE_INPUT.split(",")]


def test_sample_input() -> None:
    invalid_ids = [find_invalid_ids(id_range) for id_range in SAMPLE_ID_RANGES]
    assert invalid_id_sum(invalid_ids) == 1_227_775_554


ID_RANGE_EXPANDED_TEST_CASES: tuple[tuple[ProductIDRange, list[int]], ...] = (
    (ProductIDRange(11, 22), [11, 22]),
    (ProductIDRange(95, 115), [99, 111]),
    (ProductIDRange(998, 1012), [999, 1010]),
    (ProductIDRange(1_188_511_880, 1_188_511_890), [1_188_511_885]),
    (ProductIDRange(222_220, 222_224), [222_222]),
    (ProductIDRange(446_443, 446_449), [446_446]),
    (ProductIDRange(38_593_856, 38_593_862), [38_593_859]),
    (ProductIDRange(565_653, 565_659), [565_656]),
    (ProductIDRange(824_824_821, 824_824_827), [824_824_824]),
    (ProductIDRange(2_121_212_118, 2_121_212_124), [2_121_212_121]),
    (ProductIDRange(1_698_522, 1_698_528), []),
)


@pytest.mark.parametrize(("id_range", "truth_out"), ID_RANGE_EXPANDED_TEST_CASES)
def test_find_invalid_ids_expanded(id_range: ProductIDRange, truth_out: list[int]) -> None:
    assert find_invalid_ids(id_range, expanded=True) == truth_out


def test_sample_input_expanded() -> None:
    invalid_ids = [find_invalid_ids(id_range, expanded=True) for id_range in SAMPLE_ID_RANGES]
    assert invalid_id_sum(invalid_ids) == 4_174_379_265
