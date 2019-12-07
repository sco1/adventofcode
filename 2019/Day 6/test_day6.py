from textwrap import dedent

from aoc_2019_day6 import get_to_santa, n_total_orbits, system_from_orbits


PART_ONE = (
    dedent(
        """\
        COM)B
        B)C
        C)D
        D)E
        E)F
        B)G
        G)H
        D)I
        E)J
        J)K
        K)L
        """
    ).splitlines(),
    42,
)

PART_TWO = (
    dedent(
        """\
        COM)B
        B)C
        C)D
        D)E
        E)F
        B)G
        G)H
        D)I
        E)J
        J)K
        K)L
        K)YOU
        I)SAN
        """
    ).splitlines(),
    4,
)


def test_part_one() -> None:
    """Test for correct calculation of number of direct & indirect orbit."""
    orbit_map, truth_n_orbits = PART_ONE

    solar_system = system_from_orbits(orbit_map)
    assert n_total_orbits(solar_system) == truth_n_orbits


def test_part_two() -> None:
    """Test for correct calculation of shortest path from our orbital body to Santa's."""
    orbit_map, truth_shortest_path = PART_TWO

    solar_system = system_from_orbits(orbit_map)
    assert get_to_santa(solar_system) == truth_shortest_path
