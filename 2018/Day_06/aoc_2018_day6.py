import operator
import string
from collections import Counter, abc
from pathlib import Path

from helpers.geometry import BoundingBox, COORD, manhattan_distance


def parse_coordinates(raw_coords: str) -> tuple[list[COORD], BoundingBox]:
    """Parse the puzzle input into a list of (x,y) coordinate tuples."""
    coords = []
    for line in raw_coords.splitlines():
        x, y = (int(d) for d in line.split(","))
        coords.append((x, y))

    bbox = BoundingBox(coords)

    return coords, bbox


def build_distance_map(coordinates: abc.Iterable[COORD], bbox: BoundingBox) -> dict[COORD, int]:
    """
    Build a distance map of points within the specified bounding grid.

    Points are categorized by the ID of the closest coordinate to a given point in the grid. If the
    grid point is equally far from two or more coordinates it is excluded from the mapping.
    """
    # Calculate the bounding box for our coordinates, then map the point with the closest distance
    closest_map = {}
    for grid_coord in bbox.iter_points():
        dists = sorted(
            ((manhattan_distance(grid_coord, coord), idx) for idx, coord in enumerate(coordinates)),
            key=operator.itemgetter(0),
        )
        if dists[0][0] != dists[1][0]:
            # Points closest to two or more coordinates are ignored
            closest_map[grid_coord] = dists[0][1]

    return closest_map


def visualize_map(  # noqa: D103
    coordinates: abc.Iterable[COORD], distance_map: dict[COORD, int], bbox: BoundingBox
) -> str:
    labels = string.ascii_uppercase
    label_map = {coord: idx for idx, coord in enumerate(coordinates)}
    rows = []
    for y in bbox.y_bound:
        cols = []
        for x in bbox.x_bound:
            if (x, y) in label_map:
                # Uppercase for given coordinates
                cols.append(labels[label_map[(x, y)]])
            elif (x, y) in distance_map:
                # Lowercase for showing closest distance areas
                cols.append(labels[distance_map[(x, y)]].lower())
            else:
                # Dot for points that are closest to more than one coordinate
                cols.append(".")

        rows.append("".join(cols))

    return "\n".join(rows)


def find_finite_areas(distance_map: dict[COORD, int], bbox: BoundingBox) -> list[int]:
    """
    Calculate the areas of all bounded regions within the provided bounding box.

    A region is considered unbounded if its area extendes forever beyond the visible grid, as
    specified by the bounding box.
    """
    areas = Counter(distance_map.values())

    # Areas are infinite if they have a point on the edge of the bounding box, these are excluded
    infinite_areas = {distance_map[coord] for coord in bbox.iter_edges() if coord in distance_map}
    return sorted(areas[f_key] for f_key in (areas.keys() - infinite_areas))


def find_safe_region(
    coordinates: abc.Iterable[COORD], bbox: BoundingBox, safe_dist: int = 10_000
) -> list[COORD]:
    """
    Identify the safe locations within the region bounded by the provided coordinates.

    A location is considered safe if the total distance to all coordinates is less than the
    specified safe distance.
    """
    safe_coords = []
    for qc in bbox.iter_points():
        if sum(manhattan_distance(qc, coord) for coord in coordinates) < safe_dist:
            safe_coords.append(qc)

    return safe_coords


if __name__ == "__main__":
    puzzle_input_file = Path("puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text()

    coords, bbox = parse_coordinates(puzzle_input)
    distance_map = build_distance_map(coords, bbox)
    finite_areas = find_finite_areas(distance_map, bbox)
    print(f"Part One: {finite_areas[-1]}")
    print(f"Part Two: {len(find_safe_region(coords, bbox))}")
