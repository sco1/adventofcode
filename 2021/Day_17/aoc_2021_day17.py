import re
from pathlib import Path

BOUNDS = tuple[int, int, int, int]


def _triangular(n: int) -> int:
    """Calculate the nth triangular number."""
    return (n * (n + 1)) // 2  # Even though it can't be odd, we want an int


def parse_target_area(target_area: str) -> BOUNDS:
    """
    Parse the provided target area specification into its x & y bounds.

    Target area is assumed to be specified as `target area: x=<x_min>..<x_max>, y=<y_min>..<y_max>`.
    """
    x_min, x_max, y_min, y_max = map(int, re.findall(r"-?\d+", target_area))
    return x_min, x_max, y_min, y_max


def find_highest_y(target_area_bounds: BOUNDS) -> int:
    """
    Find the highest trajectory apex that still allows the probe to reach the target area.

    The probe is assumed to be launched at `(0,0)`, and its trajectory can be described as follows
    for each step:
        * The probe's x position increases by its x velocity
        * The probe's y position increases by its y velocity
        * Due to drag, the probe's x velocity decelerates by 1 until it reaches 0
        * Due to gravity, the probe's y velocity decreases by 1

    NOTE: This approach assumes that the x bounds are defined such that there exists an initial x
    velocity that allows the probe's x velocity to reach 0 within the target region
    """
    # Rather than brute forcing, we have the ability to come up with a closed-form expression for
    # this part of the puzzle!
    # Assuming that there exists an initial x velocity that allows the probe to reach the target
    # area with an x velocity of 0 allows us to consider y velocities without needing to ensure that
    # there exists a compatible x velocity that places the probe within the target area at the same
    # timestamp. Since they're now decoupled, we don't actually care about the x bounds; and it'll
    # turn out we don't care about y_max either!
    _, _, y_min, _ = target_area_bounds

    # https://en.wikipedia.org/wiki/Projectile_motion
    # Since we have no drag in the vertical direction, our vertical speed when the probe falls
    # back through y = 0 is going to be the same as its initial vertical launch speed. The absolute
    # fastest we can be going at this timestamp is our max target area depth per timestamp,
    # otherwise we're going to overshoot the target area in the next timestamp.
    # Now that we know our initial velocity, what's our height? Triangular numbers have returned!
    # https://en.wikipedia.org/wiki/Triangular_number
    # y = v_i + (v_i - 1) + (v_i - 2) + ... + (v_i - v_i) is the same as y = 1 + 2 + ... + v_i
    return _triangular(y_min)


def n_valid_launches(target_area_bounds: BOUNDS) -> int:
    """
    Calculate the number of `(vx, vy)` permutations that will land a probe in the target area.

    The probe is assumed to be launched at `(0,0)`, and its trajectory can be described as follows
    for each step:
        * The probe's x position increases by its x velocity
        * The probe's y position increases by its y velocity
        * Due to drag, the probe's x velocity decelerates by 1 until it reaches 0
        * Due to gravity, the probe's y velocity decreases by 1
    """
    x_min, x_max, y_min, y_max = target_area_bounds

    # Since we have some fairly decent bounds on the possible initial velocities, we can probably
    # get away with brute force here
    # For our x velocities, we have to be greater than 0 so we actually get there, and less than or
    # equal to the target area's maximum or we'll always overshoot.
    # For our y velocities, the assumption we talked about for part one gives us our upper bound
    # (-y_min), and our minimum value comes from firing it straight down so we hit at the first
    # timestep, giving us y_min
    n_valid = 0
    for v_ox in range(1, x_max + 1):
        for v_oy in range(y_min, -y_min + 1):  # y_min is always negative
            x, y = 0, 0
            v_x, v_y = v_ox, v_oy

            # Run through timestamps until we overshoot the target area
            while x <= x_max and y >= y_min:
                # Check to see if we're inside the target area
                if x >= x_min and y <= y_max:
                    n_valid += 1
                    break

                # Otherwise, continue the sim calculations
                x += v_x
                if v_x > 0:
                    # Drag force stops v_x at 0
                    v_x -= 1

                y += v_y
                v_y -= 1

    return n_valid


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()
    bounds = parse_target_area(puzzle_input)

    print(f"Part One: {find_highest_y(bounds)}")
    print(f"Part Two: {n_valid_launches(bounds)}")
