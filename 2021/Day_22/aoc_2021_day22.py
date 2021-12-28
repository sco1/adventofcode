from __future__ import annotations

import itertools
import math
import re
import typing as t
from dataclasses import dataclass, field
from pathlib import Path

INITIALIZATION_REGION = "x=-50..50,y=-50..50,z=-50..50"

# Should match one of the following patterns and extract the xyz bounds (can be negative) and the
# on/of instruction, if present:
#   * "on x=11..13,y=11..13,z=11..13"
#   * "off x=9..11,y=9..11,z=9..11"
#   * "x=-50..50,y=-50..50,z=-50..50"
INSTRUCTION_RE = re.compile(
    r"(off|on)?\s?x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)"
)


class Bounds(t.NamedTuple):  # noqa: D101
    x_min: int
    x_max: int
    y_min: int
    y_max: int
    z_min: int
    z_max: int


class Step(t.NamedTuple):  # noqa: D101
    toggle: bool | None
    bounds: Bounds


class Range(t.NamedTuple):  # noqa: D101
    left: int
    right: int


def parse_instructions(raw_steps: list[str]) -> list[Step]:
    """
    Parse the provided reactor reboot steps.

    Steps are assumed to be of the form e.g.:
        * `"on x=11..13,y=11..13,z=11..13"`
        * `"off x=9..11,y=9..11,z=9..11"`

    To help with parsing the initialization region syntax, the on/off toggle may be omitted, e.g.
    `"x=-50..50,y=-50..50,z=-50..50"`
    """
    parsed_steps = []
    for step in raw_steps:
        raw_toggle, *raw_bounds = INSTRUCTION_RE.match(step).groups()

        if raw_toggle is not None:
            if raw_toggle == "on":
                toggle = True
            else:
                toggle = False
        else:
            toggle = None

        parsed_steps.append(Step(toggle, Bounds(*(int(bound) for bound in raw_bounds))))

    return parsed_steps


def reboot_initialization_area(
    reboot_steps: list[Step], initialization_area: str = INITIALIZATION_REGION
) -> int:
    """Execute the reboot steps and count the number of online cubes in the initialization area."""
    # Since we have a bounded and relatively small cube that we care about, we can just keep track
    # of the status of all the coordinates in the initialization area
    on_coords = set()
    init_xyz = parse_instructions([initialization_area])[0].bounds
    for turn_on, step_xyz in reboot_steps:
        # For each axis, clamp the bounds to the bounds of our initialization area
        x_rng = range(max(init_xyz.x_min, step_xyz.x_min), min(step_xyz.x_max, init_xyz.x_max) + 1)
        y_rng = range(max(init_xyz.y_min, step_xyz.y_min), min(step_xyz.y_max, init_xyz.y_max) + 1)
        z_rng = range(max(init_xyz.z_min, step_xyz.z_min), min(step_xyz.z_max, init_xyz.z_max) + 1)
        # Then just hit the triple for-loop and toggle each component cube in the provided bounds
        for x, y, z in itertools.product(x_rng, y_rng, z_rng):
            if turn_on:
                on_coords.add((x, y, z))
            else:  # If we're not turning on then we're turning off
                on_coords.discard((x, y, z))

    return len(on_coords)


@dataclass
class Cuboid:  # noqa: D101
    bounds: Bounds
    off_cuboids: list[Cuboid] = field(default_factory=list)

    @staticmethod
    def _range_intersect(left: Range, right: Range) -> Range | None:
        """
        Calculate the intersection between the provided ranges.

        NOTE: `Range.left` is assumed to be <= `Range.right`
        """
        # Make sure at least one of our bounds overlaps
        if (left.left > right.right) or (right.left > left.right):
            return None

        # If there is an overlap, then it will be between the middle two of the 4 sorted limits
        arranged = sorted([*left, *right])
        return Range(arranged[1], arranged[2])

    def intersect(self, other: Cuboid) -> Cuboid | None:
        """Generate a cuboid describing the intersection between the current & query cuboids."""
        x_overlap = self._range_intersect(
            Range(self.bounds.x_min, self.bounds.x_max),
            Range(other.bounds.x_min, other.bounds.x_max),
        )
        y_overlap = self._range_intersect(
            Range(self.bounds.y_min, self.bounds.y_max),
            Range(other.bounds.y_min, other.bounds.y_max),
        )
        z_overlap = self._range_intersect(
            Range(self.bounds.z_min, self.bounds.z_max),
            Range(other.bounds.z_min, other.bounds.z_max),
        )

        # There must be an overlap on all 3 axes for the cuboids to actually intersect
        if not all((x_overlap, y_overlap, z_overlap)):
            return None

        return Cuboid(Bounds(*x_overlap, *y_overlap, *z_overlap))

    def __and__(self, other: Cuboid) -> Cuboid | None:
        return self.intersect(other)

    def turn_off(self, other: Cuboid) -> None:
        """Turn off the reactor cores bounded by the provided cuboid."""
        intersection = self & other
        if not intersection:
            # Short circuit if there's nothing to trim
            return

        # Remove any intersection from the off cuboids to prevent double counting
        for cuboid in self.off_cuboids:
            cuboid.turn_off(intersection)

        self.off_cuboids.append(intersection)

    def volume(self) -> int:
        """Calculate the volume of our cuboid."""
        return math.prod(
            (
                self.bounds.x_max - self.bounds.x_min + 1,
                self.bounds.y_max - self.bounds.y_min + 1,
                self.bounds.z_max - self.bounds.z_min + 1,
            )
        )

    def on_count(self) -> int:
        """Count the current number of active reactor cores."""
        on_vol = self.volume()  # Inclusion
        off_vol = sum(cuboid.on_count() for cuboid in self.off_cuboids)  # Exclusion

        return on_vol - off_vol


def reboot_full_reactor(reboot_steps: list[Step]) -> int:
    """Execute the reboot steps and count the number of online cubes in the reactor."""
    # While we could probably use the same approach as we did for the bounded initialization area in
    # Part 1, the ranges are so huge that it's going to take forever so we should probably do
    # something smarter.
    # One such something smarter is the inclusion–exclusion principle:
    #     https://en.wikipedia.org/wiki/Inclusion%E2%80%93exclusion_principle
    # We can apply this here by summing the "on" volume of each cuboid we interact with (our bounds
    # from each "on" instruction) and then subtracting the "off" cuboids (our bounds from each "off"
    # instruction) to give us our total "on" volume.
    cuboids: list[Cuboid] = []
    for turn_on, step_xyz in reboot_steps:
        incoming_cuboid = Cuboid(step_xyz)
        # Start by removing any instersection(s) with existing cuboids so we're not double-counting
        # either "on" or "off"
        for cuboid in cuboids:
            cuboid.turn_off(incoming_cuboid)

        # Then add back the cuboid if we're turning it on
        if turn_on:
            cuboids.append(incoming_cuboid)

    return sum(cuboid.on_count() for cuboid in cuboids)


def reboot_initialization_area_alt(
    reboot_steps: list[Step], initialization_area: str = INITIALIZATION_REGION
) -> int:
    """
    Execute the reboot steps and count the number of online cubes in the initialization area.

    This alternate solve uses the same approach as Part 2 but with a cropped area.
    """
    init_cuboid = Cuboid(parse_instructions([initialization_area])[0].bounds)

    cuboids: list[Cuboid] = []
    for turn_on, step_xyz in reboot_steps:
        incoming_cuboid = Cuboid(step_xyz)
        # Ignore any volume that's outside of our initialization area
        cropped = init_cuboid & incoming_cuboid
        if not cropped:
            continue

        # Start by removing any instersection(s) with existing cuboids so we're not double-counting
        # either "on" or "off"
        for cuboid in cuboids:
            cuboid.turn_off(cropped)

        # Then add back the cuboid if we're turning it on
        if turn_on:
            cuboids.append(cropped)

    return sum(cuboid.on_count() for cuboid in cuboids)


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().splitlines()
    reboot_steps = parse_instructions(puzzle_input)

    print(f"Part One: {reboot_initialization_area(reboot_steps)}")
    print(f"Part One (alt): {reboot_initialization_area_alt(reboot_steps)}")
    print(f"Part Two: {reboot_full_reactor(reboot_steps)}")
