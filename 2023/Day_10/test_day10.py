from textwrap import dedent

import pytest

from .aoc_2023_day10 import find_furthest_loop_point, n_enclosed_tiles, parse_map

SAMPLE_INPUT_1 = dedent(
    """\
    .....
    .S-7.
    .|.|.
    .L-J.
    .....
    """
)

SAMPLE_INPUT_2 = dedent(
    """\
    -L|F7
    7S-7|
    L|7||
    -L-J|
    L|-JF
    """
)

SAMPLE_INPUT_3 = dedent(
    """\
    ..F7.
    .FJ|.
    SJ.L7
    |F--J
    LJ...
    """
)

SAMPLE_INPUT_4 = dedent(
    """\
    7-F7-
    .FJ|7
    SJLL7
    |F--J
    LJ.LJ
    """
)

TEST_CASES = (
    (SAMPLE_INPUT_1, 4),
    (SAMPLE_INPUT_2, 4),
    (SAMPLE_INPUT_3, 8),
    (SAMPLE_INPUT_4, 8),
)


@pytest.mark.parametrize(("pipe_map", "truth_furthest_distance"), TEST_CASES)
def test_furthest_distance(pipe_map: str, truth_furthest_distance: int) -> None:
    pipe_graph, animal_start = parse_map(pipe_map)
    assert find_furthest_loop_point(pipe_graph, animal_start) == truth_furthest_distance


SQUEEZE_SAMPLE_1 = dedent(
    """\
    ...........
    .S-------7.
    .|F-----7|.
    .||.....||.
    .||.....||.
    .|L-7.F-J|.
    .|..|.|..|.
    .L--J.L--J.
    ...........
    """
)

SQUEEZE_SAMPLE_2 = dedent(
    """\
    ..........
    .S------7.
    .|F----7|.
    .||....||.
    .||....||.
    .|L-7F-J|.
    .|..||..|.
    .L--JL--J.
    ..........
    """
)

SQUEEZE_SAMPLE_3 = dedent(
    """\
    .F----7F7F7F7F-7....
    .|F--7||||||||FJ....
    .||.FJ||||||||L7....
    FJL7L7LJLJ||LJ.L-7..
    L--J.L7...LJS7F-7L7.
    ....F-J..F7FJ|L7L7L7
    ....L7.F7||L7|.L7L7|
    .....|FJLJ|FJ|F7|.LJ
    ....FJL-7.||.||||...
    ....L---J.LJ.LJLJ...
    """
)

SQUEEZE_SAMPLE_4 = dedent(
    """\
    FF7FSF7F7F7F7F7F---7
    L|LJ||||||||||||F--J
    FL-7LJLJ||||||LJL-77
    F--JF--7||LJLJ7F7FJ-
    L---JF-JLJ.||-FJLJJ7
    |F|F-JF---7F7-L7L|7|
    |FFJF7L7F-JF7|JL---7
    7-L-JL7||F7|L7F-7F7|
    L.L7LFJ|||||FJL7||LJ
    L7JLJL-JLJLJL--JLJ.L
    """
)

SQUEEZE_TEST_CASES = (
    (SQUEEZE_SAMPLE_1, 4),
    (SQUEEZE_SAMPLE_2, 4),
    (SQUEEZE_SAMPLE_3, 8),
    (SQUEEZE_SAMPLE_4, 10),
)


@pytest.mark.parametrize(("pipe_map", "truth_n_enclosed"), SQUEEZE_TEST_CASES)
def test_n_enclosed(pipe_map: str, truth_n_enclosed: int) -> None:
    pipe_graph, _ = parse_map(pipe_map)
    assert n_enclosed_tiles(pipe_graph) == truth_n_enclosed
