from __future__ import annotations

from enum import IntEnum
from itertools import product, zip_longest
from pathlib import Path
from typing import List, NamedTuple, Optional, Set, Tuple, Union


class Move(NamedTuple):
    """Represent a wiring diagram move from the previous coordinate."""

    direction: str
    dist: int


class Coordinate(NamedTuple):
    """Represent a coordinate on the wire grid."""

    x: int
    y: int

    def __eq__(self, other: Union[Coordinate, Tuple]) -> bool:
        """
        Compare x,y pairs for equality.

        Tuple comparison is supported, assuming tuple is of the form (x,y)
        """
        if isinstance(other, Coordinate):
            return self.x == other.x and self.y == other.y
        elif isinstance(other, Tuple):
            return self.x == other[0] and self.y == other[1]
        else:
            return NotImplemented

    def dist(self, other: Coordinate) -> int:
        """Calculate the Manhattan distance between x,y pairs."""
        return abs(other.x - self.x) + abs(other.y - self.y)

    def move_to(self, shift: Move) -> Coordinate:
        """
        Generate a coordinate moved by the provided `shift` parameters from the current Coordinate.

        Valid directions are: ("U": up, "D": down, "L": left, "R": right)
        """
        if shift.direction == "U":
            new_coordinate = Coordinate(x=self.x, y=self.y + shift.dist)
        elif shift.direction == "D":
            new_coordinate = Coordinate(x=self.x, y=self.y - shift.dist)
        elif shift.direction == "L":
            new_coordinate = Coordinate(x=self.x - shift.dist, y=self.y)
        elif shift.direction == "R":
            new_coordinate = Coordinate(x=self.x + shift.dist, y=self.y)
        else:
            raise ValueError(f"Unknown direction: '{shift.dir}'")

        return new_coordinate


class Orientation(IntEnum):
    """Represent the possible segment orientations."""

    HORIZONTAL = 0
    VERTICAL = 1


class Intersection(NamedTuple):
    """Represent an intersection between two Segments."""

    location: Coordinate


class Segment:
    """
    Represent the line segment spanning between two `Coordinate` instances.

    Segments are assumed to be only horizontal or vertical.
    """

    def __init__(self, start: Coordinate, end: Coordinate):
        self.start = start
        self.end = end

        self.orientation = Orientation.HORIZONTAL if start.y == end.y else Orientation.VERTICAL
        self.steps = self.build_steps()

    def build_steps(self) -> List[Coordinate]:
        """The discrete coordinate steps the wire takes."""
        if self.orientation == Orientation.HORIZONTAL:
            fill = self.start.y
        else:
            fill = self.start.x

        if self.end.x < self.start.x:
            x_range = range(self.start.x, self.end.x - 1, -1)
        else:
            x_range = range(self.start.x, self.end.x + 1)

        if self.end.y < self.start.y:
            y_range = range(self.start.y, self.end.y - 1, -1)
        else:
            y_range = range(self.start.y, self.end.y + 1)

        return list(zip_longest(x_range, y_range, fillvalue=fill))

    def __len__(self):
        """Overload len to provide the length of the segment."""
        return self.start.dist(self.end)

    def __eq__(self, other: Segment) -> bool:
        """Return True if segments share start & end points, accounting for flipping."""
        return any(
            (
                self.start == other.start and self.end == other.end,
                self.start == other.end and self.end == other.start,
            )
        )

    def __repr__(self):
        return (
            f"Segment(Coordinate({self.start.x}, {self.start.y}), "
            f"Coordinate({self.end.x}, {self.end.y}))"
        )

    def __str__(self):
        return f"Segment: ({self.start.x}, {self.start.y}) -> ({self.end.x}, {self.end.y})"

    def wire_to(self, shift: Move) -> Segment:
        """Wire a segment from the end of the current Segment using the provides `shift`."""
        return Segment(self.end, self.end.move_to(shift))

    def to_set(self) -> Set[Tuple[int, int]]:
        """Transform the Segment into a walk of cordinate pairs."""
        return set(self.steps)

    def intersect(self, other: Segment) -> Optional[Intersection]:
        """
        Check for an intersection between two segments.

        Since all segments are either horizontal or vertical, we can assume that there will be at
        most one intersection between two segments, and parallel segments will not intersect. Thanks
        Euclid!

        The case where segments overlap is ignored.
        """
        # Short-circuit for parallel segments
        if self.orientation == other.orientation:
            return

        # Deconstruct segments into a series of Coordinates & find the set intersection
        intersection = self.to_set().intersection(other.to_set())
        if not intersection:
            return

        x, y = list(intersection)[0]
        return Intersection(location=Coordinate(x=x, y=y))


class Wire:
    """Represent a wire as a series of `Segment` instances."""

    ORIGIN = Coordinate(x=0, y=0)

    def __init__(self, wiring_diagram: str):
        self._diagram = self._parse_diagram(wiring_diagram)
        self.wire_segments = self.build_wires()

    def build_wires(self) -> List[Segment]:
        """Build wire segments from the internal wiring diagram."""
        segments = [Segment(self.ORIGIN, self.ORIGIN.move_to(self._diagram[0]))]
        for step in self._diagram[1:]:
            segments.append(segments[-1].wire_to(step))

        return segments

    def intersect(self, other: Wire) -> List[Intersection]:
        """Determine the intersections between two Wires."""
        intersections = []
        for segment_a, segment_b in product(self.wire_segments, other.wire_segments):
            intersection = segment_a.intersect(segment_b)
            if intersection and intersection.location != self.ORIGIN:
                intersections.append(intersection)

        return intersections

    def closest_intersect_manhattan(self, other: Wire) -> Tuple[Coordinate, int]:
        """Find the closest intersection to the origin, by Manahattan distance, of two Wires."""
        intersection = sorted(self.intersect(other), key=lambda x: self.ORIGIN.dist(x.location))[0]

        return intersection, self.ORIGIN.dist(intersection.location)

    def closest_intersect_steps(self, other: Wire) -> Tuple[Intersection, int]:
        """Find the closest intersection to the origin, by step distance, of two Wires."""
        intersections = self.intersect(other)

        # For each intersection, iterate along each wire's path until the intersection is
        # encountered, keeping track of the number of steps taken
        distances = []
        for intersection in intersections:
            total_steps = 0
            for wire in (self, other):
                for segment in wire.wire_segments:
                    try:
                        total_steps += segment.steps.index(intersection.location)
                        break
                    except ValueError:
                        # The intersection coordinate isn't in our segment
                        total_steps += len(segment.steps) - 1

            distances.append((intersection, total_steps))

        return sorted(distances, key=lambda x: x[1])[0]

    @staticmethod
    def _parse_diagram(wiring_diagram: str) -> List[Move]:
        """
        Parse the input wiring diagram into a list of Move named tuples.

        Wiring diagrams are assumed to be of the form "R8,U15,L5,D23"
        """
        return [
            Move(direction=shift[0], dist=int(shift[1:])) for shift in wiring_diagram.split(",")
        ]


if __name__ == "__main__":
    puzzle_input = Path("./puzzle_input.txt")

    with puzzle_input.open("r") as f:
        diagram_a, diagram_b = [line.strip() for line in f]

    wire_a = Wire(diagram_a)
    wire_b = Wire(diagram_b)

    # Part 1
    print(wire_a.closest_intersect_manhattan(wire_b))

    # Part 2
    print(wire_a.closest_intersect_steps(wire_b))
