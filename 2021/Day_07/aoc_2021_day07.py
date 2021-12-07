import math
import statistics
from pathlib import Path


def _triangular_burn(crab_distances: list[int], destination: int) -> int:
    """
    Calculate the fuel burn for the crab subs to reach the specified destination.

    Fuel burn increases linearly with distance traveled (e.g traveling 1 step uses 1 fuel, 2 steps
    uses 2 fuel, etc.).

    AKA triangular numbers: https://en.wikipedia.org/wiki/Triangular_number
    """
    burn = 0
    for pos in crab_distances:
        n_steps = abs(destination - pos)
        burn += (n_steps * (n_steps + 1)) // 2  # Even though it can't be odd, we want an int

    return burn


def min_horizontal_burn(crab_distances: list[int], constant_burn: bool = True) -> int:
    """
    Calculate the fuel burn required to align the crab submarines from their starting positions.

    If `constant_burn` is `True`, then fuel burn is the same for each unit of distance regardless
    of distance traveled. Otherwise, fuel burn increases linearly with distance traveled (e.g
    traveling 1 step uses 1 fuel, 2 steps uses 2 fuel, etc.)
    """
    if constant_burn:
        # By definition, the median should be right in the middle of the data set, which should
        # result in the overall least amount of fuel used
        # Use median_low (or median_high) so we return a value from the data set if there are an
        # even number of values
        target_distance = statistics.median_low(crab_distances)
        return sum(abs(dist - target_distance) for dist in crab_distances)
    else:
        # Without a constant burn, the optimal value should be somewhere near the mean in order to
        # minimize overall distance traveled, so this is a good starting point for guesses
        dev = statistics.stdev(crab_distances)
        avg = statistics.mean(crab_distances)

        # These bounds should be wide enough to include an inflection point
        bounds = (math.floor(avg - dev), math.ceil(avg + dev))
        last_burn = float("inf")
        for guess in range(*bounds):
            burn = _triangular_burn(crab_distances, guess)
            if burn > last_burn:
                break
            else:
                last_burn = burn

        return last_burn


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = [int(distance) for distance in puzzle_input_file.read_text().strip().split(",")]

    print(f"Part One: {min_horizontal_burn(puzzle_input)}")
    print(f"Part Two: {min_horizontal_burn(puzzle_input, constant_burn=False)}")
