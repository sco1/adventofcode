from collections import defaultdict
from dataclasses import astuple, dataclass
from enum import StrEnum
from pathlib import Path

from helpers import parsing
from helpers.geometry import BoundingBox, COORD


class ReflectionType(StrEnum):  # noqa: D101
    MIRROR_DU = "/"
    MIRROR_UD = "\\"
    SPLITTER_VERT = "|"
    SPLITTER_HORIZ = "-"


def parse_cavern_map(cavern_map: str) -> tuple[dict[COORD, ReflectionType], BoundingBox]:
    """Parse the provided cavern map and map its object locations & its overall bounding box."""
    object_map = {coord: ReflectionType(c) for coord, c in parsing.parse_map_objects(cavern_map)}
    bbox = BoundingBox.enclose_map(cavern_map)

    return object_map, bbox


@dataclass
class Beam:  # noqa: D101
    x: int
    y: int
    dx: int
    dy: int

    def __post_init__(self) -> None:
        if self.dx and self.dy:
            raise ValueError("Beam can only be traveling upwards OR downwards")


DEFAULT_BEAM = Beam(x=-1, y=0, dx=1, dy=0)


def fire_beam(
    object_mapping: dict[COORD, ReflectionType],
    cavern_bbox: BoundingBox,
    beam_start: Beam = DEFAULT_BEAM,
) -> dict[COORD, int]:
    """
    Fire a beam into the chamber and determine the energy state when all beams have terminated.

    By default, the beam enters the top left corner of the cavern moving rightward. If specifying a
    custom start state, start the beam one tile outside of the cavern to ensure the entry tile is
    energized.

    The beam's behavior depends on the object it encounters as it travels:
        * If the beam encounters an empty space, it continues in the same direction.
        * If the beam encounters a mirror, the beam is reflected 9 degrees depending on the angle
        of the mirror, e.g. a beam traveling righward encountering `/` would reflect up, and if it
        was traveling leftward it would be reflected down.
        * If the beam encounters the pointy end of a splitter, the beam passes through as if it was
        an empty tile, e.g. a beam traveling rightward encountering `-` would pass straight through.
        * If the beam encounters the flat side of a splitter, the beam is split into two beams that
        travel in the direction of the splitter's ends, e.g. a beam traveling rightward encountering
        a `|` would be split into a beam traveling upwards and a beam traveling downwards.

    Beams are assumed to be traveling either horizontally OR vertically. Beams do not interact with
    other beams, and continue traveling until they hit the cavern wall. Beams may enter into a loop,
    in which case repeat visits do not add additional energy to the tile.

    A tile can have many beams passing through it at the same time, and is considered energized if
    it has more than one beam passing through it, or has had a beam split or reflected on it.
    """
    energized_tiles: dict[COORD, int] = defaultdict(int)
    beams = [beam_start]
    beams_seen = set()
    while beams:
        b = beams.pop()

        if astuple(b) in beams_seen:
            continue
        else:
            beams_seen.add(astuple(b))

        while True:
            next_loc = (b.x + b.dx, b.y + b.dy)

            # Cavern walls
            if next_loc not in cavern_bbox:
                break

            # If we haven't hit a cavern wall then we're going to energize whatever tile we travel
            # into next
            energized_tiles[next_loc] += 1

            # Empty tile
            if next_loc not in object_mapping:
                b.x, b.y = next_loc
                continue

            # Once we're here, we've hit one of our objects
            obj_hit = object_mapping[next_loc]
            if obj_hit == ReflectionType.SPLITTER_HORIZ:
                if b.dy:
                    beams.extend((Beam(*next_loc, dx=-1, dy=0), Beam(*next_loc, dx=1, dy=0)))
                    break
            elif obj_hit == ReflectionType.SPLITTER_VERT:
                if b.dx:
                    beams.extend((Beam(*next_loc, dx=0, dy=-1), Beam(*next_loc, dx=0, dy=1)))
                    break
            elif obj_hit == ReflectionType.MIRROR_DU:
                b.dx, b.dy = -b.dy, -b.dx
            elif obj_hit == ReflectionType.MIRROR_UD:
                b.dx, b.dy = b.dy, b.dx

            b.x, b.y = next_loc

    return energized_tiles


def find_max_energized(
    object_mapping: dict[COORD, ReflectionType], cavern_bbox: BoundingBox
) -> int:
    """
    Iterate over the edges of the cavern to determine which start location energizes the most tiles.

    NOTE: Beams entering from the corners can enter in both of their respective xy directions, e.g.
    the top left corner can fire both leftward and downward.
    """
    n_energized = []
    seen_state = set()
    for edge_x, edge_y in cavern_bbox.iter_edges():
        if edge_x == 0:
            # Left edge
            x, y = edge_x - 1, edge_y
            dx, dy = 1, 0
        elif edge_y == 0:
            # Top edge
            x, y = edge_x, edge_y - 1
            dx, dy = 0, 1
        elif edge_x == cavern_bbox.x_bound[-1]:
            # Right edge
            x, y = edge_x + 1, edge_y
            dx, dy = -1, 0
        elif edge_y == cavern_bbox.y_bound[-1]:
            # Left edge
            x, y = edge_x, edge_y + 1
            dx, dy = 0, -1

        # The four corners of the grid are going to appear twice since they have two starting firing
        # directions, flip their firing direction the second time they appear
        state = (x, y, dx, dy)
        if state in seen_state:
            dx, dy = -dx, -dy
        else:
            seen_state.add(state)

        beam_start = Beam(x, y, dx, dy)
        n_energized.append(len(fire_beam(object_mapping, cavern_bbox, beam_start)))

    return max(n_energized)


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    cavern_map, bbox = parse_cavern_map(puzzle_input)
    print(f"Part One: {len(fire_beam(cavern_map, bbox))}")
    print(f"Part Two: {find_max_energized(cavern_map, bbox)}")
