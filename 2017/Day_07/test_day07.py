from textwrap import dedent

from .AoC2017_Day7 import _build_tower, balance_tower, find_bottom_program

SAMPLE_TOWER = dedent(
    """\
    pbga (66)
    xhth (57)
    ebii (61)
    havc (66)
    ktlj (57)
    fwft (72) -> ktlj, cntj, xhth
    qoyq (66)
    padx (45) -> pbga, havc, qoyq
    tknk (41) -> ugml, padx, fwft
    jptl (61)
    ugml (68) -> gyxo, ebii, jptl
    gyxo (61)
    cntj (57)
    """
).splitlines()
TOWER = _build_tower(SAMPLE_TOWER)


def test_part_one() -> None:
    assert find_bottom_program(TOWER) == "tknk"


def test_part_two() -> None:
    assert balance_tower(TOWER) == 60
