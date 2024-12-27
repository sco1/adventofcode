from textwrap import dedent

import pytest

from .aoc_2024_day25 import Key, Lock, fits, n_fits, parse_schematics


def test_parse_lock() -> None:
    schematic = dedent(
        """\
        #####
        .####
        .####
        .####
        .#.#.
        .#...
        .....
        """
    )
    assert Lock.from_raw(schematic) == Lock((0, 5, 3, 4, 3))


def test_parse_key() -> None:
    schematic = dedent(
        """\
        .....
        #....
        #....
        #...#
        #.#.#
        #.###
        #####
        """
    )
    assert Key.from_raw(schematic) == Key((5, 0, 2, 1, 3))


SAMPLE_INPUT = dedent(
    """\
    #####
    .####
    .####
    .####
    .#.#.
    .#...
    .....

    #####
    ##.##
    .#.##
    ...##
    ...#.
    ...#.
    .....

    .....
    #....
    #....
    #...#
    #.#.#
    #.###
    #####

    .....
    .....
    #.#..
    ###..
    ###.#
    ###.#
    #####

    .....
    .....
    .....
    #....
    #.#..
    #.#.#
    #####
    """
)

TRUTH_LOCKS = [
    Lock((0, 5, 3, 4, 3)),
    Lock((1, 2, 0, 5, 3)),
]
TRUTH_KEYS = [
    Key((5, 0, 2, 1, 3)),
    Key((4, 3, 4, 0, 2)),
    Key((3, 0, 2, 0, 1)),
]


def test_parse_schematic() -> None:
    locks, keys = parse_schematics(SAMPLE_INPUT)

    assert locks == TRUTH_LOCKS
    assert keys == TRUTH_KEYS


FIT_TEST_CASES = (
    (Lock((0, 5, 3, 4, 3)), Key((5, 0, 2, 1, 3)), False),
    (Lock((0, 5, 3, 4, 3)), Key((4, 3, 4, 0, 2)), False),
    (Lock((0, 5, 3, 4, 3)), Key((3, 0, 2, 0, 1)), True),
    (Lock((1, 2, 0, 5, 3)), Key((5, 0, 2, 1, 3)), False),
    (Lock((1, 2, 0, 5, 3)), Key((4, 3, 4, 0, 2)), True),
    (Lock((1, 2, 0, 5, 3)), Key((3, 0, 2, 0, 1)), True),
)


@pytest.mark.parametrize(("lock", "key", "truth_fits"), FIT_TEST_CASES)
def test_key_fit(lock: Lock, key: Key, truth_fits: bool) -> None:
    assert fits(key=key, lock=lock) == truth_fits


def test_n_fits() -> None:
    locks, keys = parse_schematics(SAMPLE_INPUT)
    assert n_fits(locks, keys) == 3
