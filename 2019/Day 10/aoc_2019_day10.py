from __future__ import annotations

import math
from collections import defaultdict
from itertools import chain, islice, zip_longest
from pathlib import Path
from typing import Dict, Generator, List, NamedTuple, Tuple, Union


class Asteroid(NamedTuple):
    """Represent an asteroid as a cartesian coordinate location."""

    x: int
    y: int

    def deltas(self, other: Asteroid) -> Tuple[int, int]:
        """Calculate dx & dy for a pair of coordinates."""
        return (other.x - self.x), (other.y - self.y)

    def __eq__(self, other: Union[Asteroid, Tuple]) -> bool:
        """
        Compare x,y pairs for equality.

        Tuple comparison is supported, assuming tuple is of the form (x,y)
        """
        if isinstance(other, Asteroid):
            return self.x == other.x and self.y == other.y
        elif isinstance(other, Tuple):
            return self.x == other[0] and self.y == other[1]
        else:
            return NotImplemented


class Gradient(NamedTuple):
    """Represent an integer cartesian gradient."""

    dx: int
    dy: int

    def __eq__(self, other: Union[Gradient, Tuple]) -> bool:
        """
        Compare dx,dy pairs for equality.

        Tuple comparison is supported, assuming tuple is of the form (dx,dy)
        """
        if isinstance(other, Gradient):
            return self.dx == other.dx and self.dy == other.dy
        elif isinstance(other, Tuple):
            return self.dx == other[0] and self.dy == other[1]
        else:
            return NotImplemented

    def to_angle(self) -> int:
        """Convert gradient to degrees, clockwise from positive y-axis."""
        # Add 90 to correct for our coordinate system
        # Use mod to keep within (0, 360) degrees
        return (math.degrees(math.atan2(self.dy, self.dx)) + 90) % 360


def map_asteroids(in_map: List[str]) -> List[Asteroid]:
    """Convert the raw asteroid map into a list of asteroid x,y coordinates."""
    asteroid_coordinates = []
    for row_idx, row_contents in enumerate(in_map):
        for column_idx, column_contents in enumerate(row_contents):
            if column_contents == "#":
                asteroid_coordinates.append(Asteroid(column_idx, row_idx))

    return asteroid_coordinates


def cluster_asteroids(
    source: Asteroid, asteroid_coordinates: List[Asteroid]
) -> Dict[Gradient, List[Asteroid]]:
    """
    Cluster visible Asteroids from the provided source asteroid.

    Visible Asteroids are clustered by direction (as a Gradient namedtuple) and sorted by distance.
        * The number of keys in the returned dictionary corresponds to the number of visible
          Asteroids, as Asteroids along the same gradient are occluded by the closest
        * The first Asteroid in the list for each gradient is the visible Asteroid, all others are
          occluded
    """
    clustered_asteroids = defaultdict(list)
    for target in asteroid_coordinates:
        if target == source:
            # Avoid ourself
            continue

        dx, dy = source.deltas(target)
        normalized_dist = math.gcd(abs(dx), abs(dy))  # Use GCD to normalize & avoid floats
        grad = Gradient(dx // normalized_dist, dy // normalized_dist)

        clustered_asteroids[grad].append((normalized_dist, target))  # Store distance to sort with

    # Sort visible asteroids for each gradient direction by distance from source
    for direction in clustered_asteroids:
        clustered_asteroids[direction] = [
            target for _, target in sorted(clustered_asteroids[direction])
        ]

    return clustered_asteroids


def find_best_observation_station_location(
    asteroid_coordinates: List[Asteroid],
) -> Tuple[Asteroid, int]:
    """
    For the given Asteroid coordinates, find the optimal viewing station location.

    The number of visible Asteroids is also optionally provided.
    """
    best_location = asteroid_coordinates[0]
    best_n_visible = len(cluster_asteroids(best_location, asteroid_coordinates))
    for location in asteroid_coordinates[1:]:
        n_visible = len(cluster_asteroids(location, asteroid_coordinates))

        if n_visible > best_n_visible:
            best_location = location
            best_n_visible = n_visible

    return best_location, best_n_visible


def sweep_laser(
    source: Asteroid, asteroid_coordinates: List[Asteroid]
) -> Generator[Asteroid, None, None]:
    """
    Create a generator for the trail of destructions our asteroid laser will cause.

    The laser rotates clockwise, where 0 is assumed to be the positive y-axis. As the laser sweeps,
    if there are multiple asteroids in a given direction only one is destroyed per revolution.
    """
    clusters = cluster_asteroids(source, asteroid_coordinates)

    # Build an iterable of targets in the order their direction would be swept
    # Use itertools to chain targets together in "per-sweep" order, so asteroids that were occluded
    # by a recently destroyed asteroid will not be destroyed until the next sweep
    sorted_dirs = sorted(clusters.keys(), key=lambda x: x.to_angle())
    targets = [clusters[direction] for direction in sorted_dirs]

    return (target for target in chain.from_iterable(zip_longest(*targets)) if target)


if __name__ == "__main__":
    puzzle_input = Path("./puzzle_input.txt")

    with puzzle_input.open("r") as f:
        raw_map = [line.strip() for line in f]

    asteroid_coordinates = map_asteroids(raw_map)

    # Part 1
    best_station, n_visible = find_best_observation_station_location(asteroid_coordinates)
    print(best_station)
    print(n_visible)

    # Part 2
    # Use islice to start at the 199th element so next() gives us the 200th
    winning_asteroid = next(islice(sweep_laser(best_station, asteroid_coordinates), 199, None))
    print(winning_asteroid.x * 100 + winning_asteroid.y)
