from textwrap import dedent

import pytest

from helpers.geometry import MoveDir
from .aoc_2024_day15 import Warehouse, parse_instructions, parse_warehouse_map

SAMPLE_MAP = dedent(
    """\
    ####
    #.O#
    ##@#
    ####
    """
)

# fmt: off
TRUTH_WALLS = {(0, 1), (1, 2), (0, 0), (3, 1), (0, 3), (2, 0), (3, 0), (2, 3), (0, 2), (3, 3), (1, 0), (3, 2), (1, 3)}  # noqa: E501
TRUTH_BOXES = {(2, 1)}
TRUTH_START_LOC = (2, 2)
# fmt: on


def test_parse_warehouse_map() -> None:
    walls, boxes, start_loc = parse_warehouse_map(SAMPLE_MAP)

    assert walls == TRUTH_WALLS
    assert boxes == TRUTH_BOXES
    assert start_loc == TRUTH_START_LOC


SAMPLE_INSTRUCTIONS = "<^v^>"
TRUTH_INSTRUCTIONS = [MoveDir.WEST, MoveDir.NORTH, MoveDir.SOUTH, MoveDir.NORTH, MoveDir.EAST]


def test_parse_instructions() -> None:
    instructions = parse_instructions(SAMPLE_INSTRUCTIONS)
    assert instructions == TRUTH_INSTRUCTIONS


SHORT_EXAMPLE = dedent(
    """\
    ########
    #..O.O.#
    ##@.O..#
    #...O..#
    #.#.O..#
    #...O..#
    #......#
    ########

    <^^>>>vv<v>>v<<
    """
)

LONG_EXAMPLE = dedent(
    """\
    ##########
    #..O..O.O#
    #......O.#
    #.OO..O.O#
    #..O@..O.#
    #O#..O...#
    #O..O..O.#
    #.OO.O.OO#
    #....O...#
    ##########

    <vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
    vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
    ><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
    <<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
    ^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
    ^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
    >^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
    <><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
    ^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
    v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
    """
)

RENDERING_TEST_CASES = (
    (
        SHORT_EXAMPLE,
        dedent(
            """\
            ########
            #..O.O.#
            ##@.O..#
            #...O..#
            #.#.O..#
            #...O..#
            #......#
            ########"""
        ),
    ),
    (
        LONG_EXAMPLE,
        dedent(
            """\
            ##########
            #..O..O.O#
            #......O.#
            #.OO..O.O#
            #..O@..O.#
            #O#..O...#
            #O..O..O.#
            #.OO.O.OO#
            #....O...#
            ##########"""
        ),
    ),
)


@pytest.mark.parametrize(("raw_doc", "truth_rendered"), RENDERING_TEST_CASES)
def test_warehouse_render(raw_doc: str, truth_rendered: str) -> None:
    warehouse = Warehouse.from_raw(raw_doc)

    assert warehouse.render() == truth_rendered


EXECUTION_TEST_CASES = (
    (
        SHORT_EXAMPLE,
        dedent(
            """\
            ########
            #....OO#
            ##.....#
            #.....O#
            #.#O@..#
            #...O..#
            #...O..#
            ########"""
        ),
    ),
    (
        LONG_EXAMPLE,
        dedent(
            """\
            ##########
            #.O.O.OOO#
            #........#
            #OO......#
            #OO@.....#
            #O#.....O#
            #O.....OO#
            #O.....OO#
            #OO....OO#
            ##########"""
        ),
    ),
)


@pytest.mark.parametrize(("raw_doc", "truth_rendered"), EXECUTION_TEST_CASES)
def test_instruction_execution(raw_doc: str, truth_rendered: str) -> None:
    warehouse = Warehouse.from_raw(raw_doc)
    warehouse.execute_instructions()

    assert warehouse.render() == truth_rendered


GPS_SCORE_TEST_CASES = (
    (SHORT_EXAMPLE, 2028),
    (LONG_EXAMPLE, 10_092),
)


@pytest.mark.parametrize(("raw_doc", "truth_gps_score"), GPS_SCORE_TEST_CASES)
def test_gps_score(raw_doc: str, truth_gps_score: str) -> None:
    warehouse = Warehouse.from_raw(raw_doc)
    warehouse.execute_instructions()

    assert warehouse.calculate_gps_score() == truth_gps_score
