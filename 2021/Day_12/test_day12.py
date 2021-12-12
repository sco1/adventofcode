from textwrap import dedent

import pytest

from .aoc_2021_day12 import parse_map, path_search

TEST_CASES = [
    (
        dedent(
            """\
            start-A
            start-b
            A-c
            A-b
            b-d
            A-end
            b-end
            """
        ).splitlines(),
        10,
        36,
    ),
    (
        dedent(
            """\
            dc-end
            HN-start
            start-kj
            dc-start
            dc-HN
            LN-dc
            HN-end
            kj-sa
            kj-HN
            kj-dc
            """
        ).splitlines(),
        19,
        103,
    ),
    (
        dedent(
            """\
            fs-end
            he-DX
            fs-he
            start-DX
            pj-DX
            end-zg
            zg-sl
            zg-pj
            pj-he
            RW-he
            fs-DX
            pj-RW
            zg-RW
            start-pj
            he-WI
            zg-he
            pj-fs
            start-RW
            """
        ).splitlines(),
        226,
        3509,
    ),
]


@pytest.mark.parametrize(("raw_map", "n_routes", "n_routes_pt2"), TEST_CASES)
def test_part_one(raw_map: list[str], n_routes: int, n_routes_pt2: int) -> None:
    cave_map = parse_map(raw_map)
    assert path_search(cave_map, "start", set()) == n_routes


@pytest.mark.parametrize(("raw_map", "n_routes", "n_routes_pt2"), TEST_CASES)
def test_part_two(raw_map: list[str], n_routes: int, n_routes_pt2: int) -> None:
    cave_map = parse_map(raw_map)
    assert path_search(cave_map, "start", set(), duplicate_seen=False) == n_routes_pt2
