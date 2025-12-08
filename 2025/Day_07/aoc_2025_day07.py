from pathlib import Path

from helpers.geometry import BoundingBox, COORD
from helpers.parsing import parse_map_objects


def parse_diagram(diagram: str) -> tuple[COORD, set[COORD], BoundingBox]:
    """
    Parse the provided tachyon manifold diagram into its components.

    The tachyon beam is assumed to enter the manifold at the location marked by `"S"`. Locations
    marked by `"^"` are assumed to contain a beam splitter; these locations are returned. Locations
    marked with `"."` are assumed to be empty space and are ignored.

    A helper bounding box is also included that bounds the entirety of the provided diagram,
    including empty space.
    """
    start = None
    splitters = set()
    for coord, c in parse_map_objects(diagram):
        if c == "S":
            start = coord
        elif c == "^":
            splitters.add(coord)

    if start is None:
        raise ValueError("Could not locate beam entrance location.")

    rows = diagram.splitlines()
    width = len(rows[0])
    height = len(rows)

    bbox = BoundingBox.from_dims(width=width, height=height)

    return start, splitters, bbox


def fire_beam(start: COORD, splitters: set[COORD], bbox: BoundingBox) -> tuple[int, int]:
    """
    Fire the tachyon beam from the provided start location and measure the beam behavior.

    Two quantities are measured by this simulation:
        1. The first measurement assumes that when a beam encounters a splitter, the beam is stopped
           and a new tachyon beam continues from the immediate left and right of the splitter; beams
           do not overlap. The first measurement is the total number of splits until the beams exit
           the manifold.
        2. The second measurement assumes a quantum tachyon manifold; only a single particle is sent
           through! If the particle encounters a splitter, it takes both the left and right paths of
           each splitter. The second measurement is the total number of timelines present after the
           particle exits the manifold.
    """
    beams = [0] * len(bbox.y_bound)  # Track our beam timelines
    n_splits = 0
    for x, y in bbox.iter_points(row_major=True):  # Ensure we're iterating line-by-line
        if (x, y) == start:
            beams[x] += 1

        if (x, y) in splitters:
            # Once we hit a splitter, start a new timeline in each direction
            beams[x - 1] += beams[x]
            beams[x + 1] += beams[x]

            # For the the splitting measurement, only add a split if there is not already a beam in
            # this column
            if beams[x] > 0:
                n_splits += 1

            # Since we've hit a splitter, stop the beam from traveling any further
            beams[x] = 0

    # Once we've tracked everything through the manifold, beams should have tracked the number of
    # times a particle has exited the manifold in each position; summing this will give us our total
    # number of timelines
    return n_splits, sum(beams)


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    n_splits, n_timelines = fire_beam(*parse_diagram(puzzle_input))

    print(f"Part One: {n_splits}")
    print(f"Part Two: {n_timelines}")
