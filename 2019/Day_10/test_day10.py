from itertools import islice
from textwrap import dedent

import pytest
from aoc_2019_day10 import find_best_observation_station_location, map_asteroids, sweep_laser


# Test cases provided as (asteroid map, truth x, truth y, truth asteroids seen)
PART_ONE = [
    (
        dedent(
            """\
            .#..#
            .....
            #####
            ....#
            ...##
            """
        ),
        3,
        4,
        8,
    ),
    (
        dedent(
            """\
            ......#.#.
            #..#.#....
            ..#######.
            .#.#.###..
            .#..#.....
            ..#....#.#
            #..#....#.
            .##.#..###
            ##...#..#.
            .#....####
            """
        ),
        5,
        8,
        33,
    ),
    (
        dedent(
            """\
            #.#...#.#.
            .###....#.
            .#....#...
            ##.#.#.#.#
            ....#.#.#.
            .##..###.#
            ..#...##..
            ..##....##
            ......#...
            .####.###.
            """
        ),
        1,
        2,
        35,
    ),
    (
        dedent(
            """\
            .#..#..###
            ####.###.#
            ....###.#.
            ..###.##.#
            ##.##.#.#.
            ....###..#
            ..#.#..#.#
            #..#.#.###
            .##...##.#
            .....#.#..
            """
        ),
        6,
        3,
        41,
    ),
    (
        dedent(
            """\
            .#..##.###...#######
            ##.############..##.
            .#.######.########.#
            .###.#######.####.#.
            #####.##.#.##.###.##
            ..#####..#.#########
            ####################
            #.####....###.#.#.##
            ##.#################
            #####.##.###..####..
            ..######..##.#######
            ####.##.####...##..#
            .#####..#.######.###
            ##...#.##########...
            #.##########.#######
            .####.#.###.###.#.##
            ....##.##.###..#####
            .#.#.###########.###
            #.#.#.#####.####.###
            ###.##.####.##.#..##
            """
        ),
        11,
        13,
        210,
    ),
]

# Test cases provided as (asteroid map, truth x, truth y)
PART_TWO = [
    (
        dedent(
            """\
            .#..##.###...#######
            ##.############..##.
            .#.######.########.#
            .###.#######.####.#.
            #####.##.#.##.###.##
            ..#####..#.#########
            ####################
            #.####....###.#.#.##
            ##.#################
            #####.##.###..####..
            ..######..##.#######
            ####.##.####...##..#
            .#####..#.######.###
            ##...#.##########...
            #.##########.#######
            .####.#.###.###.#.##
            ....##.##.###..#####
            .#.#.###########.###
            #.#.#.#####.####.###
            ###.##.####.##.#..##
            """
        ),
        8,
        2,
    ),
]


@pytest.mark.parametrize("asteroid_map, truth_x, truth_y, truth_n_asteroids_seen", PART_ONE)
def test_part_one(
    asteroid_map: str, truth_x: int, truth_y: int, truth_n_asteroids_seen: int
) -> None:
    """Test that the given map yields the optimal asteroid-based observation station location."""
    asteroid_coordinates = map_asteroids(asteroid_map.split("\n"))
    best_station, n_visible = find_best_observation_station_location(asteroid_coordinates)

    assert (truth_x, truth_y) == best_station
    assert truth_n_asteroids_seen == n_visible


@pytest.mark.parametrize("asteroid_map, truth_x, truth_y", PART_TWO)
def test_part_two(asteroid_map: str, truth_x: int, truth_y: int) -> None:
    """Test that the given map yields the correct 200th asteroid to be lasered."""
    asteroid_coordinates = map_asteroids(asteroid_map.split("\n"))
    best_station, _ = find_best_observation_station_location(asteroid_coordinates)
    winning_asteroid = next(islice(sweep_laser(best_station, asteroid_coordinates), 199, None))

    assert (truth_x, truth_y) == winning_asteroid
