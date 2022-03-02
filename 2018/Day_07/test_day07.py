from textwrap import dedent

from .aoc_2018_day7 import _parse_edges, determine_step_order, elf_assembly

SAMPLE_INSTRUCTIONS = dedent(
    """\
    Step C must be finished before step A can begin.
    Step C must be finished before step F can begin.
    Step A must be finished before step B can begin.
    Step A must be finished before step D can begin.
    Step B must be finished before step E can begin.
    Step D must be finished before step E can begin.
    Step F must be finished before step E can begin.
    """
).splitlines()
EDGES = _parse_edges(SAMPLE_INSTRUCTIONS)


def test_part_one() -> None:
    assert determine_step_order(EDGES) == "CABDFE"


def test_part_two() -> None:
    assert elf_assembly(EDGES, n_workers=2, base_time=0) == 15
