import itertools
from collections import defaultdict
from pathlib import Path

from helpers.geometry import BoundingBox, COORD, slope
from helpers.parsing import parse_map_objects


def parse_antenna_map(raw_map: str) -> tuple[dict[str, set[COORD]], BoundingBox]:
    """
    Parse the provided antenna map into its components.

    The provided raw map is assumed to represent an XY grid of points in the subject region, where
    empty locations are denoted by `.` and antenna locations are marked by a single lowercase
    letter, uppercase letter, or digit.

    For example, the following region contains 5 antennas, 4 with a `0` frequency and 1 with an `A`
    frequency:

    ```
    ........0...
    .....0......
    .......0....
    ....0.......
    ......A.....
    ```

    Antenna coordinates are grouped by frequency and returned, along with the map's bounding box.
    """
    map_bbox = BoundingBox.enclose_map(raw_map)

    antenna_locations = defaultdict(set)
    for loc, c in parse_map_objects(raw_map):
        antenna_locations[c].add(loc)

    return antenna_locations, map_bbox


def find_antinodes(
    antenna_locations: dict[str, set[COORD]], bbox: BoundingBox, add_resonant: bool = False
) -> dict[str, set[COORD]]:
    """
    Find all antinode locations within the mapped regions based on the provided antenna locations.

    An antinode occurs at any point that is perfectly in line with two antennas of the same
    frequency. The number of antinodes generated depends on whether or not resonance is taken into
    account:
        * If resonance is not taken into account (`add_resonant=False`), for any pair of antennas
        with the same frequency there are two antinodes, one on either side of them.
        * If resonance is being taken into account (`add_resonant=True`), an antinode occurs at any
        grid position exactly in line with at least two antennas of the same frequency. Note that
        this also includes the locations of the base antennas of the pair, as they are in-line with
        each other.

    For either case, the distance of each antinode away from their source antenna is the same as the
    distance between the base antenna pair.
    """
    antinodes: dict[str, set[COORD]] = defaultdict(set)
    for freq, antennas in antenna_locations.items():
        if len(antennas) <= 1:  # Antinodes require a pair of antennas
            continue

        for ant_a, ant_b in itertools.combinations(antennas, 2):
            ant_dx, ant_dy = slope(ant_a, ant_b)

            if add_resonant:
                # If we're considering resonant antinodes, continue in each direction outward from
                # each of the base antennas until we've exited the bounds of the map
                # The base antennas are also in line with each other so they will have an antinode
                # at their position as well
                antinodes[freq] |= {ant_a, ant_b}
                for base, direction in ((ant_a, -1), (ant_b, 1)):
                    i = 1
                    while True:
                        dx, dy = (i * direction * ant_dx), (i * direction * ant_dy)
                        potential_antinode = (base[0] + dx, base[1] + dy)

                        if potential_antinode in bbox:
                            antinodes[freq].add(potential_antinode)
                        else:
                            break

                        i += 1
            else:
                # Without considering resonant antinodes, each pair of antennas will create one
                # antinode outward in-line with the antenna pair
                for base, direction in ((ant_a, -1), (ant_b, 1)):
                    dx, dy = (direction * ant_dx), (direction * ant_dy)
                    potential_antinode = (base[0] + dx, base[1] + dy)

                    if potential_antinode in bbox:
                        antinodes[freq].add(potential_antinode)

    return antinodes


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    antenna_locations, map_bbox = parse_antenna_map(puzzle_input)

    antinode_locations = find_antinodes(antenna_locations, map_bbox)
    unique_antinodes: set[COORD] = set()
    unique_antinodes.update(*antinode_locations.values())

    print(f"Part One: {len(unique_antinodes)}")

    resonant_antinodes = find_antinodes(antenna_locations, map_bbox, add_resonant=True)
    resonant_unique_antinodes: set[COORD] = set()
    resonant_unique_antinodes.update(*resonant_antinodes.values())
    print(f"Part Two: {len(resonant_unique_antinodes)}")
