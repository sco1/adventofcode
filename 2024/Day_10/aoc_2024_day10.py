from collections import deque
from pathlib import Path

from helpers.geometry import COORD, iter_neighbors
from helpers.parsing import parse_map_objects


def parse_topo_map(raw_map: str) -> tuple[dict[COORD, int], set[COORD]]:
    """
    Parse the provided topographic hiking map into its components of interest.

    The topographic map is assumed to be provided as a grid of integers indicating the height at
    each position using a scale from 0 (lowest) to 9 (highest), e.g. :

    ```
    0123
    1234
    8765
    9876
    ```

    Trailheads are assumed to begin at any location in the grid where the height is `0`.

    A mapping of grid coordinate -> height is provided, along with the trailhead location(s).
    """
    topo_map = {}
    trailheads = set()
    for coord, c in parse_map_objects(raw_map):
        height = int(c)
        topo_map[coord] = height

        if height == 0:
            trailheads.add(coord)

    return topo_map, trailheads


def find_good_trails(topo_map: dict[COORD, int], trailheads: set[COORD]) -> int:
    """
    Calculate the trailhead score for the provided topographic hiking map parameters.

    A trailhead's score is the number of `9`-height positions reachable from that trailhead via a
    good hiking trail. A good hiking trail is any path that starts at height `0`, ends at height
    `9`, and always increases by a height of exactly `1` at each step. Hiking trails never include
    diagonal steps.
    """
    n_good = 0
    for th in trailheads:
        hike_steps = deque([th])
        seen_peaks = set()
        while hike_steps:
            start = hike_steps.popleft()
            for step in iter_neighbors(start):
                if step not in topo_map:
                    continue

                dh = topo_map[step] - topo_map[start]
                if dh == 1:
                    if topo_map[step] == 9:
                        if step not in seen_peaks:
                            seen_peaks.add(step)
                            n_good += 1
                    else:
                        hike_steps.append(step)

    return n_good


def find_all_trails(topo_map: dict[COORD, int], trailheads: set[COORD]) -> int:
    """
    Calculate the total number of distinct good hiking trails in the provided topographic map.

    A good hiking trail is any path that starts at height `0`, ends at height `9`, and always
    increases by a height of exactly `1` at each step. Hiking trails never include diagonal steps.
    """
    hike_steps = deque(trailheads)
    n_good = 0
    while hike_steps:
        start = hike_steps.popleft()
        for step in iter_neighbors(start):
            if step not in topo_map:
                continue

            dh = topo_map[step] - topo_map[start]
            if dh == 1:
                if topo_map[step] == 9:
                    n_good += 1
                else:
                    hike_steps.append(step)

    return n_good


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    topo_map, trailheads = parse_topo_map(puzzle_input)

    print(f"Part One: {find_good_trails(topo_map, trailheads)}")
    print(f"Part Two: {find_all_trails(topo_map, trailheads)}")
