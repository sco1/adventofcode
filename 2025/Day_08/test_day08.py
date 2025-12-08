import math

import pytest

from .aoc_2025_day08 import connect_all, connect_n_closest, junction_pdist, parse_junctions

SAMPLE_INPUT = """\
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
"""

TRUTH_JUNCTIONS = [
    (162, 817, 812),
    (57, 618, 57),
    (906, 360, 560),
    (592, 479, 940),
    (352, 342, 300),
    (466, 668, 158),
    (542, 29, 236),
    (431, 825, 988),
    (739, 650, 466),
    (52, 470, 668),
    (216, 146, 977),
    (819, 987, 18),
    (117, 168, 530),
    (805, 96, 715),
    (346, 949, 466),
    (970, 615, 88),
    (941, 993, 340),
    (862, 61, 35),
    (984, 92, 344),
    (425, 690, 689),
]

TRUTH_DISTANCES = [
    (316.90, (162, 817, 812), (425, 690, 689)),
    (321.56, (162, 817, 812), (431, 825, 988)),
    (322.37, (906, 360, 560), (805, 96, 715)),
]


def test_parse_junctions() -> None:
    junctions = parse_junctions(SAMPLE_INPUT)
    assert junctions == TRUTH_JUNCTIONS


def test_parse_junction_pdist() -> None:
    pdist = junction_pdist(TRUTH_JUNCTIONS)
    assert len(pdist) == math.comb(len(TRUTH_JUNCTIONS), 2)

    for i, truth_item in enumerate(TRUTH_DISTANCES):
        truth_dist, truth_p, truth_q = truth_item
        dist, p, q = pdist[i]

        assert dist == pytest.approx(truth_dist, rel=1e-3)
        assert p == truth_p
        assert q == truth_q


def test_connect_n_closest() -> None:
    assert connect_n_closest(TRUTH_JUNCTIONS, n=10) == 40


def test_connect_all() -> None:
    assert connect_all(TRUTH_JUNCTIONS) == 25_272
