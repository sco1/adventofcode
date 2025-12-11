from pathlib import Path

import networkx as nx


def parse_network(network_spec: str) -> nx.DiGraph:
    """
    Parse the provided network specification into a directed graph of its devices.

    The network specification is assumed to be a newline-delimited sequence of devices of the
    following form: `<device>: <output(s)>`, where outputs can be one or more space-delimited
    identifiers. Device & output specifiers are interpreted as strings.

    The network is modeled as a directed graph whose edges are connections between the source
    device and its output(s); data can only flow in one direction from a device to its outputs.
    """
    g = nx.DiGraph()
    for device_spec in network_spec.splitlines():
        source, outputs = device_spec.split(":")
        g.add_edges_from((source, o) for o in outputs.split())

    return g


def count_paths(network: nx.DiGraph, source: str = "you", dest: str = "out") -> int:
    """Count the number of paths from the specified source & destination devices."""
    missing = {source, dest} - network.nodes
    if missing:
        raise ValueError(f"Network graph missing one or more required nodes: {missing}")

    n_paths = 0
    for _ in nx.all_simple_paths(network, source, dest):
        n_paths += 1

    return n_paths


def count_problem_paths(network: nx.DiGraph) -> int:
    """
    Count the number of problem paths in the provided network specification.

    Paths are considered from the server rack (`"svr"`) to the output device (`"out"`); a path is
    considered a problem if it visits both the digital-to-analog converter (`"dac"`) and a fast
    Fourier transform device (`"fft"`) along its journey.
    """
    missing = ({"svr", "out", "dac", "fft"}) - network.nodes
    if missing:
        raise ValueError(f"Network graph missing one or more required nodes: {missing}")

    # The full problem set is way too large to just naively iterate through all the paths and check
    # for containment. We can instead break it down as a sum of products of subpaths:
    # svr -> dac * dac -> fft * fft -> out + svr -> fft * fft -> dac * dac -> out
    chunks = [
        [("svr", "dac"), ("dac", "fft"), ("fft", "out")],
        [("svr", "fft"), ("fft", "dac"), ("dac", "out")],
    ]  # I'm sure there's a way to generalize this but I just wanted to get something working

    n_problem = 0
    for c in chunks:
        sub = 1
        for src, dest in c:
            sub *= len(tuple(nx.all_simple_paths(network, src, dest)))

        n_problem += sub

    return n_problem


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    nw = parse_network(puzzle_input)

    print(f"Part One: {count_paths(nw)}")
    print(f"Part Two: {...}")
