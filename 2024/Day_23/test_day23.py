from textwrap import dedent

from .aoc_2024_day23 import find_n_length_connections, find_password, find_t_cliques, parse_lan_map

SAMPLE_INPUT = dedent(
    """\
    kh-tc
    qp-kh
    de-cg
    ka-co
    yn-aq
    qp-ub
    cg-tb
    vc-aq
    tb-ka
    wh-tc
    yn-cg
    kh-ub
    ta-co
    de-co
    tc-td
    tb-wq
    wh-td
    ta-ka
    td-qp
    aq-cg
    wq-ub
    ub-vc
    de-ta
    wq-aq
    wq-vc
    wh-yn
    ka-de
    kh-ta
    co-tc
    wh-qp
    tb-vc
    td-yn
    """
)


def test_3_cliques() -> None:
    lan_map = parse_lan_map(SAMPLE_INPUT)

    TRUTH_CLIQUES = {
        frozenset(("aq", "cg", "yn")),
        frozenset(("aq", "vc", "wq")),
        frozenset(("co", "de", "ka")),
        frozenset(("co", "de", "ta")),
        frozenset(("co", "ka", "ta")),
        frozenset(("de", "ka", "ta")),
        frozenset(("kh", "qp", "ub")),
        frozenset(("qp", "td", "wh")),
        frozenset(("tb", "vc", "wq")),
        frozenset(("tc", "td", "wh")),
        frozenset(("td", "wh", "yn")),
        frozenset(("ub", "vc", "wq")),
    }

    assert find_n_length_connections(lan_map, 3) == TRUTH_CLIQUES


def test_find_t_3_cliques() -> None:
    lan_map = parse_lan_map(SAMPLE_INPUT)

    TRUTH_CLIQUES = {
        frozenset({"co", "de", "ta"}),
        frozenset({"co", "ka", "ta"}),
        frozenset({"de", "ka", "ta"}),
        frozenset({"qp", "td", "wh"}),
        frozenset({"tb", "vc", "wq"}),
        frozenset({"tc", "td", "wh"}),
        frozenset({"td", "wh", "yn"}),
    }

    assert find_t_cliques(lan_map, 3) == TRUTH_CLIQUES


def test_find_password() -> None:
    lan_map = parse_lan_map(SAMPLE_INPUT)
    assert find_password(lan_map) == "co,de,ka,ta"
