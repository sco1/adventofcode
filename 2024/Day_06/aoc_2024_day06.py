from pathlib import Path

from helpers.geometry import BoundingBox, COORD, MoveDir
from helpers.parsing import parse_map_objects


def parse_lab_map(raw_map: str) -> tuple[COORD, set[COORD], BoundingBox]:
    """
    Parse the provided raw laboratory map into its components.

    The raw laboratory map is assumed to contain newline-delimited ASCII mapping of coordinates
    contained by the lab: empty spaces are denoted by `.`, obstacles are denoted by `#`, and the
    guard's starting position is denoted by `^`.

    The guard's starting position is returned, along with the locations of any obstacles and a
    bounding box for the entire laboratory.
    """
    lab_bbox = BoundingBox.enclose_map(raw_map)

    start_loc = None
    obstructions = set()
    for coord, c in parse_map_objects(raw_map):
        if c == "^":
            start_loc = coord

        if c == "#":
            obstructions.add(coord)

    if start_loc is None:
        raise ValueError("Could not locate guard start location")

    return start_loc, obstructions, lab_bbox


def walk_patrol(start_loc: COORD, obstructions: set[COORD], lab_bbox: BoundingBox) -> set[COORD]:
    """
    Simulate the guard's laboratory patrol and determine the coordinates visited during patrol.

    It is assumed that the guard begins facing up (i.e. North), and walks forward until either an
    obstacle blocks their way or they exit the mapped lab space. If a blocking obstacle is
    encountered, the guard turns 90 degrees to the right before continuing.

    NOTE: The guard's starting position is included in the set of visited locations.
    """
    visited = set()
    loc = start_loc
    facing = MoveDir.NORTH
    while loc in lab_bbox:
        visited.add(loc)

        next_loc = facing.shift(loc)
        if next_loc in obstructions:
            facing = facing.rot_90()
        else:
            loc = next_loc

    return visited


def trap_guard(start_loc: COORD, obstructions: set[COORD], lab_bbox: BoundingBox) -> set[COORD]:
    """
    Identify coordinates where an obstacle can be placed to force the guard to patroll for eternity.

    NOTE: The guard's starting position is excluded from consideration. They would probably notice.
    """
    # Narrow the search space by first determining which points the guard would visit on a regular
    # patrol
    regular_visited = walk_patrol(start_loc, obstructions, lab_bbox)
    regular_visited.remove(start_loc)

    # Let's try the brute force approach first and see if the time taken is tolerable
    # Modify the walk to include facing direction as well
    looper_objs = set()
    for ob_c in regular_visited:
        visited = set()
        loc = start_loc
        facing = MoveDir.NORTH
        obstructions.add(ob_c)

        while loc in lab_bbox:
            state = (loc, facing)
            if state in visited:
                # We've reached this point before while facing the same direction
                looper_objs.add(ob_c)
                break

            visited.add((loc, facing))

            next_loc = facing.shift(loc)
            if next_loc in obstructions:
                facing = facing.rot_90()
            else:
                loc = next_loc

        obstructions.remove(ob_c)  # Reset obstructions to initial conditions

    return looper_objs


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    start_loc, obstructions, lab_bbox = parse_lab_map(puzzle_input)
    visited = walk_patrol(start_loc, obstructions, lab_bbox)

    print(f"Part One: {len(visited)}")

    looper_objs = trap_guard(start_loc, obstructions, lab_bbox)
    print(f"Part Two: {len(looper_objs)}")
