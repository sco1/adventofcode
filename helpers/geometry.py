import itertools
import typing as t
from collections import abc
from enum import Enum
from functools import cached_property

import more_itertools as miter

COORD: t.TypeAlias = tuple[int, int]


class MoveDir(Enum):
    """2D Neighbor deltas, assuming the y-axis points downward."""

    NORTHWEST = (-1, -1)
    NORTH = (0, -1)
    NORTHEAST = (1, -1)
    EAST = (1, 0)
    SOUTHEAST = (1, 1)
    SOUTH = (0, 1)
    SOUTHWEST = (-1, 1)
    WEST = (-1, 0)

    def shift(self, start: COORD) -> COORD:
        """Apply the enumerated deltas to the provided start coordinate."""
        x, y = start
        dx, dy = self.value
        return (x + dx, y + dy)


DIAGONALS = {MoveDir.NORTHWEST, MoveDir.NORTHEAST, MoveDir.SOUTHEAST, MoveDir.SOUTHWEST}


def iter_neighbors(
    start: COORD, include_diagonal: bool = False
) -> abc.Generator[COORD, None, None]:
    """
    Iterate over the 2D neighbors of the provided coordinate.

    Use the `include_diagonal` flag to include diagonal neighbors.

    NOTE: It is assumed that the y-axis points downwards.
    NOTE: Iteration order is dependent on the definition of the `MoveDir` enum.
    """
    for move in MoveDir:
        if not include_diagonal and move in DIAGONALS:
            continue

        yield move.shift(start)


def get_bounds(coords: abc.Iterable[abc.Sequence[int]], padding: int = 0) -> tuple[range, ...]:
    """
    Calculate the bounding range(s) for each dimension of the provided coordinates.

    An integer `padding` width may be provided to create a uniform padding around the provided
    boundary.

    NOTE: Coordinates can be of any dimension, but it is assumed that all coordinates are of the
    same dimension.
    """
    if not coords:
        raise ValueError("Cannot find bounds of an empty collection.")

    if padding < 0:
        raise ValueError(f"Padding spec cannot be a negative number. Received: {padding}")

    seekable_coords = miter.seekable(coords)
    n_dims = len(next(seekable_coords))

    bounds = []
    for dim in range(n_dims):
        seekable_coords.seek(0)
        lbound, rbound = miter.minmax((coord[dim] for coord in seekable_coords))

        bounds.append(range(lbound - padding, rbound + 1 + padding))

    return tuple(bounds)


class BoundingBox:
    """Simple bounding box for the provided coordinates, supporting membership testing."""

    def __init__(self, coords: abc.Iterable[COORD]) -> None:
        self.x_bound, self.y_bound = get_bounds(coords)

    @cached_property
    def area(self) -> int:  # noqa: D102
        return len(self.x_bound) * len(self.y_bound)

    def __contains__(self, query: COORD) -> bool:
        x, y = query
        return x in self.x_bound and y in self.y_bound

    def iter_points(self) -> abc.Iterable[COORD]:
        """Iterate over all coordinates contained in the bounding box."""
        for coord in itertools.product(self.x_bound, self.y_bound):
            yield coord

    def iter_edges(self) -> abc.Iterable[COORD]:
        """Iterate over the edge coordinates of the bounding box."""
        # top/bottom
        for coord in itertools.product((self.x_bound[0], self.x_bound[-1]), self.y_bound):
            yield coord

        # left/right
        for coord in itertools.product(self.x_bound, (self.y_bound[0], self.y_bound[-1])):
            yield coord


def manhattan_distance(p1: COORD, p2: COORD) -> int:
    """
    Calculate the Manhattan distance between the provided pair of 2D coordinates.

    See: https://en.wikipedia.org/wiki/Taxicab_geometry
    """
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
