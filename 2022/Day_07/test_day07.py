from textwrap import dedent

import pytest

from .aoc_2022_day07 import calculate_candidate_dir_size, find_best_deletion, parse_terminal_session

SAMPLE_SESSION = dedent(
    """\
    $ cd /
    $ ls
    dir a
    14848514 b.txt
    8504156 c.dat
    dir d
    $ cd a
    $ ls
    dir e
    29116 f
    2557 g
    62596 h.lst
    $ cd e
    $ ls
    584 i
    $ cd ..
    $ cd ..
    $ cd d
    $ ls
    4060174 j
    8033020 d.log
    5626152 d.ext
    7214296 k
    """
)
DIR_SIZES = parse_terminal_session(SAMPLE_SESSION.splitlines())


SAMPLE_SIZE_OF = (
    ("/a/e/", 584),
    ("/a/", 94_853),
    ("/d/", 24_933_642),
    ("/", 48_381_165),
)


@pytest.mark.parametrize(("query_dir", "truth_size"), SAMPLE_SIZE_OF)
def test_size_of(query_dir: str, truth_size: int) -> None:
    assert DIR_SIZES[query_dir] == truth_size


def test_dir_size_calc() -> None:
    assert calculate_candidate_dir_size(DIR_SIZES) == 95_437


def test_best_deletion() -> None:
    assert find_best_deletion(DIR_SIZES) == 24_933_642
