from typing import List

import pytest
from aoc_2019_day8 import check_image, load_image, merge_layers


# Provide test cases as (raw stream, width, height, check value) tuples
PART_ONE = [
    ("123456789012", 3, 2, 1),
]

# Provide test cases as (raw stream, width, height, merged image) tuples
PART_TWO = [
    ("0222112222120000", 2, 2, [[0, 1], [1, 0]]),
]


@pytest.mark.parametrize("raw_stream, width, height, truth_check", PART_ONE)
def test_part_one(raw_stream: str, width: int, height: int, truth_check: int) -> None:
    """Test that the provided raw stream yields the correct check value when processed."""
    image = load_image(raw_stream, width=width, height=height)
    assert check_image(image) == truth_check


@pytest.mark.parametrize("raw_stream, width, height, truth_image", PART_TWO)
def test_part_two(raw_stream: str, width: int, height: int, truth_image: List[List[int]]) -> None:
    """Test that the provided raw stream yields the correctly merged layers."""
    image = load_image(raw_stream, width=width, height=height)
    merged_image = merge_layers(image)

    assert merged_image.tolist() == truth_image
