from collections import defaultdict, deque
from pathlib import Path

from helpers.geometry import BoundingBox, COORD, MoveDir, iter_neighbors
from helpers.parsing import parse_hashed_map


def run_sim(elf_coords: set[COORD], n_rounds: int = 10) -> int:
    """
    Simulate the Elven planting process for `n_rounds` and calculate the amount of ground covered.

    At the beginning of each round, each elf considers its 8 neighboring locations; if the elf has
    no neighbors then it does not move during the round. Otherwise, the elf cycles through each of
    the cardinal directions and proposes movement in the first direction that has no adjacent elves
    (e.g. move North if there is no elf in the N, NE, or NW positions). Once each elf has indicated
    their proposed move, the elves move to these proposed positions if and only if they are the only
    elf to do so. At the end of each round, the order of the proposal directions rotates, putting
    the first direction at the end (e.g. NSWE becomes SWEN).

    Once the specified number of rounds has been simulated, the area of the Elves' bounding box is
    calculated, and the number of open spaces is returned.
    """
    # Define at the function level since we're going to be rotating it
    check_dirs = deque(
        (
            (MoveDir.NORTH, (MoveDir.NORTH, MoveDir.NORTHEAST, MoveDir.NORTHWEST)),
            (MoveDir.SOUTH, (MoveDir.SOUTH, MoveDir.SOUTHEAST, MoveDir.SOUTHWEST)),
            (MoveDir.WEST, (MoveDir.WEST, MoveDir.NORTHWEST, MoveDir.SOUTHWEST)),
            (MoveDir.EAST, (MoveDir.EAST, MoveDir.NORTHEAST, MoveDir.SOUTHEAST)),
        )
    )

    for _ in range(n_rounds):
        proposed: dict[COORD, list[COORD]] = defaultdict(list)
        for x, y in elf_coords:
            # At least one neighbor must be occupied for the elf to move
            if all(
                check not in elf_coords for check in iter_neighbors((x, y), include_diagonal=True)
            ):
                continue

            # Propose first matching move direction
            for direction, check_deltas in check_dirs:
                if all(delta.shift((x, y)) not in elf_coords for delta in check_deltas):
                    proposed[direction.shift((x, y))].append((x, y))
                    break

        # If only one elf wants to move to a specified position then they'll move
        will_move = {
            destination: elves[0] for destination, elves in proposed.items() if len(elves) == 1
        }
        moved = set(will_move.values())
        elf_coords = (elf_coords - moved) | will_move.keys()

        # At the end of each round, first considered direction is moved to the end
        check_dirs.rotate(-1)

    # Calculate the number of open spaces inside the Elves' bounding box
    n_elves = len(elf_coords)
    bbox = BoundingBox(elf_coords)
    return bbox.area - n_elves


def run_until_static(elf_coords: set[COORD]) -> int:
    """
    Simulate the Elven planting process until a round is encountered with no movement.

    At the beginning of each round, each elf considers its 8 neighboring locations; if the elf has
    no neighbors then it does not move during the round. Otherwise, the elf cycles through each of
    the cardinal directions and proposes movement in the first direction that has no adjacent elves
    (e.g. move North if there is no elf in the N, NE, or NW positions). Once each elf has indicated
    their proposed move, the elves move to these proposed positions if and only if they are the only
    elf to do so. At the end of each round, the order of the proposal directions rotates, putting
    the first direction at the end (e.g. NSWE becomes SWEN).

    Once a round without movement is detected, its index is returned.
    """
    # Define at the function level since we're going to be rotating it
    check_dirs = deque(
        (
            (MoveDir.NORTH, (MoveDir.NORTH, MoveDir.NORTHEAST, MoveDir.NORTHWEST)),
            (MoveDir.SOUTH, (MoveDir.SOUTH, MoveDir.SOUTHEAST, MoveDir.SOUTHWEST)),
            (MoveDir.WEST, (MoveDir.WEST, MoveDir.NORTHWEST, MoveDir.SOUTHWEST)),
            (MoveDir.EAST, (MoveDir.EAST, MoveDir.NORTHEAST, MoveDir.SOUTHEAST)),
        )
    )

    # Easiest to just copy+paste from Part 1 with a different loop condition instead of being clever
    n_steps = 0
    while True:
        n_steps += 1
        proposed: dict[COORD, list[COORD]] = defaultdict(list)
        for x, y in elf_coords:
            # At least one neighbor must be occupied for the elf to move
            if all(
                check not in elf_coords for check in iter_neighbors((x, y), include_diagonal=True)
            ):
                continue

            # Propose first matching move direction
            for direction, check_deltas in check_dirs:
                if all(delta.shift((x, y)) not in elf_coords for delta in check_deltas):
                    proposed[direction.shift((x, y))].append((x, y))
                    break

        # If only one elf wants to move to a specified position then they'll move
        will_move = {
            destination: elves[0] for destination, elves in proposed.items() if len(elves) == 1
        }
        moved = set(will_move.values())
        if not moved:
            return n_steps

        elf_coords = (elf_coords - moved) | will_move.keys()

        # At the end of each round, first considered direction is moved to the end
        check_dirs.rotate(-1)


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text()

    start_coords = parse_hashed_map(puzzle_input)
    print(f"Part One: {run_sim(start_coords)}")
    print(f"Part Two: {run_until_static(start_coords)}")
