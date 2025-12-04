from pathlib import Path

from helpers.geometry import BoundingBox, COORD, iter_neighbors
from helpers.parsing import parse_hashed_map


def find_accessible_rolls(roll_locations: set[COORD]) -> set[COORD]:
    """
    Locate rolls of paper that are accessible by the Elves' forklift.

    A roll of paper is deemed accessible if it has fewer than four rolls of paper adjacent to it,
    including diagonals. It is assumed that the storage area is bound by walls on all sides.
    """
    bbox = BoundingBox(roll_locations)

    accessible_rolls = set()
    for loc in roll_locations:
        n_adjacent_rolls = 0
        for n in iter_neighbors(loc, include_diagonal=True):
            if n not in bbox:
                continue

            if n in roll_locations:
                n_adjacent_rolls += 1

        if n_adjacent_rolls < 4:
            accessible_rolls.add(loc)

    return accessible_rolls


def remove_all_accessible(roll_locations: set[COORD]) -> int:
    """
    Determine the total number of rolls of paper that are potentially accessible by the forklift.

    A simulation is run where a roll of paper is removed as soon as it can be accessed. The
    simulation continues until no roll is accessible to the forklift.
    """
    n_removed = 0
    while True:
        accessible_rolls = find_accessible_rolls(roll_locations)
        if not accessible_rolls:
            break

        n_removed += len(accessible_rolls)
        roll_locations -= accessible_rolls

    return n_removed


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    print(f"Part One: {len(find_accessible_rolls(parse_hashed_map(puzzle_input, marker="@")))}")
    print(f"Part Two: {remove_all_accessible(parse_hashed_map(puzzle_input, marker="@"))}")
