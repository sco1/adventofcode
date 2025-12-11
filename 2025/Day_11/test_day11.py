import pytest

from .aoc_2025_day11 import count_paths, count_problem_paths, parse_network

SAMPLE_INPUT_A = """\
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
"""

SAMPLE_INPUT_B = """\
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
"""

NETWORK_PARSING_CASES = (
    (SAMPLE_INPUT_A, 11, 17),
    (SAMPLE_INPUT_B, 14, 16),
)


@pytest.mark.parametrize(("network_spec", "truth_n_nodes", "truth_n_edges"), NETWORK_PARSING_CASES)
def test_parse_network(network_spec: str, truth_n_nodes: int, truth_n_edges: int) -> None:
    # Not worth doing a full check, just a simple dimension check should be fine
    nw = parse_network(network_spec)

    assert len(nw.nodes) == truth_n_nodes
    assert len(nw.edges) == truth_n_edges


def test_count_paths() -> None:
    nw = parse_network(SAMPLE_INPUT_A)
    assert count_paths(nw) == 5


def test_count_problem_paths() -> None:
    nw = parse_network(SAMPLE_INPUT_B)
    assert count_problem_paths(nw) == 2
