import dataclasses
from functools import partial
from textwrap import dedent

import pytest

from .aoc_2023_day05 import Mapping, iter_seeds, parse_almanac

MAPPING_CASES = (
    ("50 98 2", [98, 99], [50, 51]),
    ("52 50 48", list(range(50, 98)), list(range(52, 100))),
)

MAPPING_P = partial(Mapping.from_str, source="src", dest="")


@pytest.mark.parametrize(("map_str", "truth_src", "truth_dest"), MAPPING_CASES)
def test_mapping_parse(map_str: str, truth_src: list[int], truth_dest: list[int]) -> None:
    mapping = MAPPING_P(map_str)
    assert list(mapping._source_range) == truth_src
    assert [mapping[src_idx] for src_idx in mapping._source_range] == truth_dest


SAMPLE_INPUT = dedent(
    """\
    seeds: 79 14 55 13

    seed-to-soil map:
    50 98 2
    52 50 48

    soil-to-fertilizer map:
    0 15 37
    37 52 2
    39 0 15

    fertilizer-to-water map:
    49 53 8
    0 11 42
    42 0 7
    57 7 4

    water-to-light map:
    88 18 7
    18 25 70

    light-to-temperature map:
    45 77 23
    81 45 19
    68 64 13

    temperature-to-humidity map:
    0 69 1
    1 0 69

    humidity-to-location map:
    60 56 37
    56 93 4
    """
)

TRUTH_END_STATE = (
    (79, 81, 81, 81, 74, 78, 78, 82),
    (14, 14, 53, 49, 42, 42, 43, 43),
    (55, 57, 57, 53, 46, 82, 82, 86),
    (13, 13, 52, 41, 34, 34, 35, 35),
)


def test_seed_state() -> None:
    seed_idx, mappings = parse_almanac(SAMPLE_INPUT)
    seed_state = list(iter_seeds(seed_idx, mappings))
    for seed, truth_state in zip(seed_state, TRUTH_END_STATE):
        assert dataclasses.astuple(seed) == truth_state


def test_seed_ranges() -> None:
    seed_idx, mappings = parse_almanac(SAMPLE_INPUT, use_seed_range=True)
    seed_state = list(iter_seeds(seed_idx, mappings))
    assert len(seed_state) == 27
    assert min(seed.location for seed in seed_state) == 46
