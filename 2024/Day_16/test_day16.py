from textwrap import dedent

import pytest

from .aoc_2024_day16 import calculate_lowest_score, n_seat_locations, parse_reindeer_map

SAMPLE_INPUT = dedent(
    """\
    ###############
    #.......#....E#
    #.#.###.#.###.#
    #.....#.#...#.#
    #.###.#####.#.#
    #.#.#.......#.#
    #.#.#####.###.#
    #...........#.#
    ###.#.#####.#.#
    #...#.....#.#.#
    #.#.#.###.#.#.#
    #.....#...#.#.#
    #.###.#.#.#.#.#
    #S..#.....#...#
    ###############
    """
)

ANOTHER_SAMPLE_INPUT = dedent(
    """\
    #################
    #...#...#...#..E#
    #.#.#.#.#.#.#.#.#
    #.#.#.#...#...#.#
    #.#.#.#.###.#.#.#
    #...#.#.#.....#.#
    #.#.#.#.#.#####.#
    #.#...#.#.#.....#
    #.#.#####.#.###.#
    #.#.#.......#...#
    #.#.###.#####.###
    #.#.#...#.....#.#
    #.#.#.#####.###.#
    #.#.#.........#.#
    #.#.#.#########.#
    #S#.............#
    #################
    """
)

LOW_SCORE_TEST_CASES = (
    (SAMPLE_INPUT, 7036),
    (ANOTHER_SAMPLE_INPUT, 11_048),
)


@pytest.mark.parametrize(("maze_map", "truth_lowest_score"), LOW_SCORE_TEST_CASES)
def test_find_low_score(maze_map: str, truth_lowest_score: int) -> None:
    maze, start = parse_reindeer_map(maze_map)
    assert calculate_lowest_score(maze, start) == truth_lowest_score


SEAT_LOCATIONS_TEST_CASES = (
    (SAMPLE_INPUT, 45),
    (ANOTHER_SAMPLE_INPUT, 64),
)


@pytest.mark.parametrize(("maze_map", "truth_n_seats"), SEAT_LOCATIONS_TEST_CASES)
def test_n_seat_locations(maze_map: str, truth_n_seats: int) -> None:
    maze, start = parse_reindeer_map(maze_map)
    assert n_seat_locations(maze, start) == truth_n_seats
