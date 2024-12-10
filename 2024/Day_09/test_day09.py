import pytest

from .aoc_2024_day09 import FileBlock, calculate_checksum, defrag, defrag_continuous, parse_disk_map

SAMPLE_INPUT = "12345"
TRUTH_BLOCKS = [
    FileBlock(id_=0, n_blocks=1, n_free=2),
    FileBlock(id_=1, n_blocks=3, n_free=4),
    FileBlock(id_=2, n_blocks=5, n_free=0),
]


def test_parse_disk_map() -> None:
    parsed_blocks = parse_disk_map(SAMPLE_INPUT)
    assert parsed_blocks == TRUTH_BLOCKS


DISK_MAP_TEST_CASES = (
    ("12345", "0..111....22222"),
    ("2333133121414131402", "00...111...2...333.44.5555.6666.777.888899"),
)


@pytest.mark.parametrize(("raw_map", "truth_printed"), DISK_MAP_TEST_CASES)
def test_block_display(raw_map: str, truth_printed: str) -> None:
    parsed_blocks = parse_disk_map(raw_map)
    rendered = "".join(str(b) for b in parsed_blocks)
    assert rendered == truth_printed


DEFRAG_TEST_CASES = (
    ("12345", "022111222......"),
    ("2333133121414131402", "0099811188827773336446555566.............."),
)


@pytest.mark.parametrize(("raw_map", "truth_defragged"), DEFRAG_TEST_CASES)
def test_defrag(raw_map: str, truth_defragged: str) -> None:
    parsed_blocks = parse_disk_map(raw_map)
    defragged = defrag(parsed_blocks)

    assert "".join(str(v) for v in defragged) == truth_defragged


CHECKSUM_TEST_CASES = (
    ("0099811188827773336446555566..............", 1928),
    ("00992111777.44.333....5555.6666.....8888..", 2858),
)


@pytest.mark.parametrize(("raw_disk_map", "truth_checksum"), CHECKSUM_TEST_CASES)
def test_checksum(raw_disk_map: str, truth_checksum: int) -> None:
    disk_map: list[int | str] = []
    for c in raw_disk_map:
        if c == ".":
            disk_map.append(c)
        else:
            disk_map.append(int(c))

    assert calculate_checksum(disk_map) == truth_checksum


CONTINUOUS_DEFRAG_TEST_CASES = (
    ("2333133121414131402", "00992111777.44.333....5555.6666.....8888.."),
    ("1313165", "021......33333......"),
)


@pytest.mark.parametrize(("raw_map", "truth_defragged"), CONTINUOUS_DEFRAG_TEST_CASES)
def test_continuous_defrag(raw_map: str, truth_defragged: str) -> None:
    parsed_blocks = parse_disk_map(raw_map)
    defragged = defrag_continuous(parsed_blocks)

    assert "".join(str(v) for v in defragged) == truth_defragged
