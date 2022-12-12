from textwrap import dedent

import networkx as nx

from .aoc_2022_day12 import build_valid_steps, find_shortest_hike, parse_map

SAMPLE_MAP = dedent(
    """
    Sabqponm
    abcryxxl
    accszExk
    acctuvwj
    abdefghi
    """
)


def test_part_one() -> None:
    elevation, start_pos, end_pos = parse_map(SAMPLE_MAP)
    valid_steps = build_valid_steps(elevation)
    assert nx.shortest_path_length(valid_steps, start_pos, end_pos) == 31


def test_part_two() -> None:
    elevation, start_pos, end_pos = parse_map(SAMPLE_MAP)
    valid_steps = build_valid_steps(elevation)

    assert find_shortest_hike(elevation, valid_steps, end_pos) == 29
