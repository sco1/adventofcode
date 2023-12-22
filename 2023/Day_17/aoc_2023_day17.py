from heapq import heappop, heappush
from pathlib import Path

from helpers.geometry import COORD
from helpers.parsing import parse_map_objects

# (dx, dy) tuples for possible move directions: URDL
VELOCITIES = {(0, 1), (1, 0), (0, -1), (-1, 0)}


def parse_heat_map(raw_map: str) -> dict[COORD, int]:
    """
    Parse the provided heat raw heat map.

    The heat map is assumed to be provided as lines of single-digit positive integers (no
    delimiter), mapping the heat loss for the given coordinate.
    """
    return {coord: int(v) for coord, v in parse_map_objects(raw_map)}


def minimize_heat_loss(
    heat_map: dict[COORD, int], min_n_straight: int = 1, max_n_straight: int = 3
) -> int:
    """
    Calculate the minimum heat loss required to move from the top left to bottom right of the map.

    Crucibles are top-heavy and pushed by hand & are very difficult to move in a straight line for
    very long. The crucible must move at least `min_n_straight` spaces in a direction, accumulating
    heat along the way, and at most `max_n_straight` spaces in a direction before turning. Crucibles
    must turn 90 degrees left or right, and cannot reverse direction.
    """
    # Dijkstra is back! https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    start = (0, 0)
    end = max(heat_map)  # With every coordinate mapped, the bottom right will be the max coordinate

    seen = set()  # (coord, (dx, dy))
    move_queue = [(0, start, (0, 0))]  # heat, coord, (dx, dy)
    while move_queue:
        total_heat, curr, vel = heappop(move_queue)
        if curr == end:
            return total_heat

        if (curr, vel) in seen:
            continue
        seen.add((curr, vel))

        # Other than the starting point, once we're here we can only turn 90 degrees from the
        # direction we're currently going in; we cannot go backwards or continue in a straight line
        cdx, cdy = vel
        possible_velocities = VELOCITIES - {vel, (-cdx, -cdy)}
        for dx, dy in possible_velocities:
            heat = total_heat
            x, y = curr
            # Crucible can move up to max_n times in this direction
            for n in range(1, max_n_straight + 1):
                x, y = x + dx, y + dy
                if (x, y) in heat_map:
                    heat += heat_map[(x, y)]

                    # For ultra crucibles, they have to move at least min_n times in this direction,
                    # and accumulate heat along the way
                    if n >= min_n_straight:
                        heappush(move_queue, (heat, (x, y), (dx, dy)))

    return -1


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    heat_map = parse_heat_map(puzzle_input)
    print(f"Part One: {minimize_heat_loss(heat_map)}")
    print(f"Part Two: {minimize_heat_loss(heat_map, min_n_straight=4, max_n_straight=10)}")
