from collections import defaultdict
from pathlib import Path


def parse_map(raw_map: list[str]) -> defaultdict:
    """
    Parse the provided cave map into an adjacency graph.

    Connections (edges) between caves (nodes) are assumed to be provided as a list of
    `"<to>-<from>"` strings.

    NOTE: Node names are case sensitive.
    """
    cave_map = defaultdict(list)
    for connection in raw_map:
        to, from_ = connection.strip().split("-")
        cave_map[to].append(from_)
        cave_map[from_].append(to)

    return cave_map


def _is_small_cave(cave: str) -> bool:
    """Check if the cave is a small cave, which have all-lowercase names."""
    return cave == cave.lower()


def path_search(
    cave_map: defaultdict, current_cave: str, visited: set, duplicate_seen: bool = True
) -> int:
    """
    Count the number of safe passages available for navigation through the input cave system.

    For safe, non-boring passage it is assumed that no small caves (denoted by lowercase cave names)
    are visited more than once. If a small cave is particularly interesting, the `duplicate_seen`
    flag may be set at the initial invocation to allow visitation of a single small cave twice
    during our travels.
    """
    # We've reached the exit, yay!
    if current_cave == "end":
        return 1

    # Check for duplicate small cave visits
    if _is_small_cave(current_cave) and (current_cave in visited):
        if current_cave == "start":
            # Don't get caught in a cycle at the start
            return 0

        # For Part One, no duplicate visits of small caves are allowed
        # For Part Two, only one small cave is allowed to be visited twice, so once we see it then
        # our small cave visiting behavior becomes the same as what we have for Part One
        if duplicate_seen:
            return 0
        else:
            duplicate_seen = True

    # Now past the short-circuits, into the recursive DFS
    # Create a new set so we're not accidentally passing around a reference to the same set
    visited = visited | {current_cave}
    n_valid_paths = 0
    for connected_cave in cave_map[current_cave]:
        n_valid_paths += path_search(cave_map, connected_cave, visited, duplicate_seen)

    return n_valid_paths


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().splitlines()
    cave_map = parse_map(puzzle_input)

    print(f"Part One: {path_search(cave_map, 'start', set())}")
    print(f"Part Two: {path_search(cave_map, 'start', set(), False)}")
