import itertools
import typing as t
from pathlib import Path


def _spiralizer() -> t.Generator[tuple[int, int], None, None]:
    """Spiral outward from `(0,0)` and yield coordinate tuples for each location."""
    # Initial conditions
    x = y = 0
    dx, dy = (0, -1)  # This gets inverted to (1,0) at step 0, which is how we want to start

    while True:
        # Change our dx/dy when we hit a corner to continue the spiral
        if any(
            (
                x > 0 and y == 1 - x,  # Bottom right
                x == y,  # Origin, top right & bottom left
                x < 0 and y == -x,  # Top Left
            )
        ):
            dx, dy = -dy, dx

        x, y = (x + dx), (y + dy)
        yield x, y


def walk_spiral(target_square: int) -> int:
    """
    Calculate the shortest path required to reach the target square in the memory spiral.

    Memory is allocated by starting at square 1 and counting up while spiraling outward. The
    shortest path is calculated as the manhattan distance between the location of the target square
    and the start point.
    """
    # Initial conditions
    step = 1
    x = y = 0

    memory_location = _spiralizer()
    while True:
        if step == target_square:
            return abs(x) + abs(y)

        step += 1
        x, y = next(memory_location)


def _adjacent(x: int, y: int) -> t.Generator[tuple[int, int], None, None]:
    """Yield coordinates for the adjacent elements of the provided coordinate."""
    for dx, dy in itertools.product((-1, 0, 1), repeat=2):
        if dx == dy == 0:  # Skip self reference
            continue

        yield x + dx, y + dy


def stress_test(target_value: int) -> int:
    """
    Spiral memory system stress test.

    To stress test the system, the memory grid is initialized with a value of `1` at square `1`.
    Then, as the spiral is walked the sum of all adjacent squares is stored in the square to
    initialize it. Once a square is written, its value does not change.

    This initialization process is continued until the first value is written that is larger than
    the provided target value. This value is returned for debugging purposes.
    """
    # Initial conditions
    x = y = 0
    val = 1
    memory_location = _spiralizer()
    memory_values = {(x, y): val}

    while val <= target_value:
        x, y = next(memory_location)
        val = 0
        for neighbor in _adjacent(x, y):
            val += memory_values.get(neighbor, 0)

        memory_values[(x, y)] = val

    return val


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = int(puzzle_input_file.read_text().strip())

    print(f"Part One: {walk_spiral(puzzle_input)}")
    print(f"Part Two: {stress_test(puzzle_input)}")
