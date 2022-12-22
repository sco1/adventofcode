from __future__ import annotations

import itertools
import typing as t
from pathlib import Path
from textwrap import dedent

COORD: t.TypeAlias = tuple[int, int]


def _get_bounds(piece_comp: t.Iterable[COORD]) -> tuple[range, range]:
    """Calculate the bounding ranges for the bounding box containing the provided coordinates."""
    bounds = []
    for dim in (0, 1):
        lbound = min(comp[dim] for comp in piece_comp)
        rbound = max(comp[dim] for comp in piece_comp)

        # Include the max
        bounds.append(range(lbound, rbound + 1))

    return tuple(bounds)  # type: ignore[return-value]


class Elfomino:  # noqa: D101
    def __init__(self, coords: t.Iterable[COORD]) -> None:
        self.coords = frozenset(coords)

        w_bound, h_bound = _get_bounds(coords)
        self.width = max(w_bound) + 1
        self.height = max(h_bound)

    def __matmul__(self, delta: tuple[int, int]) -> set[COORD]:
        """Shift the Elfomino to the specified origin & emit the shifted coordinates."""
        dx, dy = delta
        return {(x + dx, y + dy) for x, y in self.coords}

    def peek(self, delta: tuple[int, int]) -> set[COORD]:
        """Shift the Elfomino to the specified origin & emit the shifted coordinates."""
        return self @ delta

    @classmethod
    def from_raw(cls, raw_spec: str) -> Elfomino:
        """
        Parse newline-delimited Elfominos from the provided specification.

        The origin of the parsed Elfomino is assumed to be the bottom left of its raw spec.
        """
        coords = set()
        split_spec = raw_spec.splitlines()
        height = len(split_spec)
        for y, line in enumerate(raw_spec.splitlines()):
            for x, c in enumerate(line):
                if c == "#":
                    coords.add((x, (height - y)))

        return cls(coords)


SHAPE_SPEC = dedent(
    """\
    ####

    .#.
    ###
    .#.

    ..#
    ..#
    ###

    #
    #
    #
    #

    ##
    ##
    """
)
PIECES = tuple(Elfomino.from_raw(piece) for piece in SHAPE_SPEC.split("\n\n"))


def _try_jet_push(
    piece: Elfomino, start: COORD, jet_dir: str, solid: set[COORD], tunnel_width: int
) -> int:
    """
    Attempt to push the given Elfomino with the provided jet and give the resulting X position.

    If the Elfomino is unable to move as requested, either because it would impact the wall or an
    existing piece, the X position is returned unchanged. Otherwise, it is moved 1 unit in the jet
    direction, assumed to be `"<"` for left (`x-1`) and `"<"` for right (`x+1`).
    """
    x, y = start
    if jet_dir == "<":
        nx = x - 1
        if x == 0 or (solid & piece @ (nx, y)):
            return x
        else:
            return nx
    elif jet_dir == ">":
        nx = x + 1
        if x == (tunnel_width - piece.width) or (solid & piece @ (nx, y)):
            return x
        else:
            return nx
    else:
        raise ValueError(f"Unknown jet direction: '{jet_dir}'")


def sim_n_pieces(
    jet_scan: str,
    piece_spec: t.Iterable[Elfomino] = PIECES,
    n_pieces: int = 2022,
    tunnel_width: int = 7,
) -> int:
    """
    Run the ~~Tetris game~~ rock simulation for the given iterations & calculate total tower height.

    `jet_scan` is assumed to be a description of the tunnel's jet pattern, given as a single line
    string containing one or more `"<"` or `">"` characters.

    Rock pieces and jet patterns are assumed to cycle for the life of the simulation.

    After a rock appears, it alternates between being pushed by a jet of hot gas one unit and then
    falling one unit down. If any movement would cause any part of the rock to move into the walls,
    floor, or a stopped rock, the movement instead does not occur. If a downward movement would have
    caused a falling rock to move into the floor or an already-fallen rock, the falling rock stops
    where it is (having landed on something) and a new rock immediately begins falling.
    """
    pieces = itertools.cycle(piece_spec)
    jets = itertools.cycle(jet_scan)

    total_height = 0
    solid = set(((x, 0) for x in range(tunnel_width)))  # Initialize with the floor coordinates
    for _ in range(n_pieces):
        piece = next(pieces)

        # Each rock appears 2 units from the left edge & 3 units above the current highest point
        x, y = (2, total_height + 3)

        while True:
            # Pieces fall until they hit either another piece or the floor
            x = _try_jet_push(piece, (x, y), next(jets), solid, tunnel_width)

            vert_peek = piece @ (x, y - 1)
            if solid & vert_peek:
                final = piece @ (x, y)
                final_max_y = max(sy for _, sy in final)

                solid |= final
                total_height = max(final_max_y, total_height)
                break
            else:
                y -= 1

    return total_height


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    print(f"Part One: {sim_n_pieces(puzzle_input, n_pieces=2_022)}")
    # print(f"Part Two: {sim_n_pieces(puzzle_input, n_pieces=1_000_000_000_000)}")
