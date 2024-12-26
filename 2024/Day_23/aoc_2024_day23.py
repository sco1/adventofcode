from pathlib import Path

import networkx as nx


def parse_lan_map(connections: str) -> nx.Graph:
    """
    Parse the provided LAN map into its graph representation.

    The LAN map is assumed to be provided as a newline-delimited list of every connection between
    two computers, where connections are not directional, e.g.:

    ```
    kh-tc
    qp-kh
    de-cg
    ka-co
    ```
    """
    lan_map = nx.Graph()

    for conn in connections.splitlines():
        left, right = conn.split("-")
        lan_map.add_edge(left, right)

    return lan_map


def find_n_length_connections(lan_map: nx.Graph, n: int = 3) -> set[frozenset[str]]:
    """Locate all `n`-sized cliques of connected computers from the provided LAN map."""
    n_len_cliques = set()
    for c in nx.enumerate_all_cliques(lan_map):
        # Networkx's iteration is ordered by cardinality, so we can stop after we reach the desired
        # clique length
        if len(c) < n:
            continue
        if len(c) > n:
            break

        n_len_cliques.add(frozenset(c))

    return n_len_cliques


def find_t_cliques(lan_map: nx.Graph, n: int = 3) -> set[frozenset[str]]:
    """Locate all `n`-sized cliques where at least one computer name begins with `'t'`."""
    n_len_cliques = find_n_length_connections(lan_map, n)
    t_cliques = set()
    for c in n_len_cliques:
        if any(cn.startswith("t") for cn in c):
            t_cliques.add(c)

    return t_cliques


def find_password(lan_map: nx.Graph) -> str:
    """
    Obtain the password for the LAN party given the provided LAN connection map.

    The desired LAN party is the largest set of computers that are all conected to each other. The
    password for this party is the name of every connected computer, sorted alphabetically, then
    joined together with commas.

    For example, the password for the LAN party described by:

    ```
    ka-co
    ta-co
    de-co
    ```

    Would be `"co,de,ka,ta"`
    """
    # Networkx's iteration is ordered by cardinality, so we can exhaust the iterator and take the
    # last clique in order to avoid having to dump the entire collection of cliques into memory
    for c in nx.enumerate_all_cliques(lan_map):  # noqa: B007
        continue

    return ",".join(sorted(c))


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    lan_map = parse_lan_map(puzzle_input)

    print(f"Part One: {len(find_t_cliques(lan_map))}")
    print(f"Part Two: {find_password(lan_map)}")
