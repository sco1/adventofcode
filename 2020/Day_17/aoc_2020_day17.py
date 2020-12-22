import itertools as it
import typing as t
from collections import abc
from pathlib import Path

# Rather than play flippy doodle with indices, the X axis runs along the rows & Y axis along the
# columns. This makes debugging easier on my brain :)
COORD3D = tuple[int, int, int]
COORD4D = tuple[int, int, int, int]


class ConwayCube:
    """Simulation for the North Pole's super-secret imaging satellites' power supply."""

    # In an ideal world I'd make generalized coordinate generators, but copy+paste is easier for AOC

    def __init__(self, starting_slice: str, ndims: int = 3) -> None:
        # This approach will be similar to the seat map from Day 11, but with a set instead of a
        # dict. There's no real point in having the dict when we were really just keeping track of
        # occupied coordinates.
        self.active_cells = self.parse_slice(starting_slice, ndims)
        self._ndims = ndims

        self._step = 0

    @property
    def n_active(self) -> int:
        """Return a count of the number of currently active cells in the grid."""
        return len(self.active_cells)

    def cube_coords(self) -> abc.Iterator[COORD3D]:
        """
        Yield coordinate triples for the grid surrounding & including the active energy cubes.

        Because the dimension is infinite, the coordinates that form the "border" around the
        currently activated cubes needs to be checked along with the space inside.
        """
        # Find min/max coordinates for the 3 dimensions
        sx, sy, sz = self.active_cells.pop()  # Pop & put back since we can't index a set
        self.active_cells.add((sx, sy, sz))
        minx = maxx = sx
        miny = maxy = sy
        minz = maxz = sz

        for x, y, z in self.active_cells:
            if x < minx:
                minx = x
            if x > maxx:
                maxx = x

            if y < miny:
                miny = y
            if y > maxy:
                maxy = y

            if z < minz:
                minz = z
            if z > maxz:
                maxz = z

        # Build iteration ranges, to include the "border" around the currently active cells
        xrange = range(minx - 1, maxx + 2)
        yrange = range(miny - 1, maxy + 2)
        zrange = range(minz - 1, maxy + 2)

        for x, y, z in it.product(xrange, yrange, zrange):
            yield x, y, z

    def hypercube_coords(self) -> abc.Iterator[COORD4D]:
        """
        Yield coordinate quadruples for the grid surrounding & including the active energy cubes.

        Because the dimension is infinite, the coordinates that form the "border" around the
        currently activated cubes needs to be checked along with the space inside.
        """
        # Find min/max coordinates for the 4 dimensions
        sx, sy, sz, sw = self.active_cells.pop()  # Pop & put back since we can't index a set
        self.active_cells.add((sx, sy, sz, sw))
        minx = maxx = sx
        miny = maxy = sy
        minz = maxz = sz
        minw = maxw = sw

        for x, y, z, w in self.active_cells:
            if x < minx:
                minx = x
            if x > maxx:
                maxx = x

            if y < miny:
                miny = y
            if y > maxy:
                maxy = y

            if z < minz:
                minz = z
            if z > maxz:
                maxz = z

            if w < minw:
                minw = w
            if w > maxw:
                maxw = w

        # Build iteration ranges, to include the "border" around the currently active cells
        xrange = range(minx - 1, maxx + 2)
        yrange = range(miny - 1, maxy + 2)
        zrange = range(minz - 1, maxy + 2)
        wrange = range(minw - 1, maxw + 2)

        for x, y, z, w in it.product(xrange, yrange, zrange, wrange):
            yield x, y, z, w

    def step_sim(self) -> None:
        """
        Simulate a cycle of the energy source.

        For each cycle, all neighbors of the currently active cells are considered.
            * If a cube is active an exactly 2 or 3 of its neighbors are also active, the cube
            remains active, otherwise it becomes inactive.
            * If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes
            inactive, otherwise it remains inactive.

        NOTE: All state changes are assumed to occur simultaneously.
        """
        new_cells = set()

        if self._ndims == 3:
            coord_gen = self.cube_coords
            neighbor_gen = self.neighbors_3d
        elif self._ndims == 4:
            coord_gen = self.hypercube_coords
            neighbor_gen = self.neighbors_4d

        for check_cell in coord_gen():
            n_active_neighbors = sum(
                1
                for neighbor_cell in neighbor_gen(check_cell)
                if neighbor_cell in self.active_cells
            )
            if check_cell in self.active_cells:
                if n_active_neighbors in (2, 3):
                    new_cells.add(check_cell)
            else:
                if n_active_neighbors == 3:
                    new_cells.add(check_cell)

        self.active_cells = new_cells
        self._step += 1

    def step_n(self, n: int = 6) -> None:
        """Step the cube through `n` iterations."""
        for _ in range(n):
            self.step_sim()

    @staticmethod
    def parse_slice(starting_slice: str, ndims: int) -> t.Union[set[COORD3D], set[COORD4D]]:
        """
        Parse the provided starting slice into a set of active cell coordinates.

        The starting slice is assumed to be a multiline string mapping out the initial slice of the
        pocket dimension, where `"."` represents an inactive cube and `"#"` represents an active
        cube.
        """
        active_cells = set()
        for row_idx, row in enumerate(starting_slice.splitlines()):
            for col_idx, val in enumerate(row):
                if val == "#":
                    if ndims == 3:
                        # Starting slice is at z = 0
                        active_cells.add((row_idx, col_idx, 0))
                    if ndims == 4:
                        # Starting slice is at z = 0, w = 0
                        active_cells.add((row_idx, col_idx, 0, 0))

        return active_cells

    @staticmethod
    def neighbors_3d(start_coord: COORD3D) -> abc.Iterator[COORD3D]:
        """
        Yield coordinate triples for neighbors of the provided start coordinate.

        NOTE: The self reference `(0, 0, 0)` is ignored.
        """
        for dx, dy, dz in it.product((-1, 0, 1), repeat=3):
            if (dx, dy, dz) == (0, 0, 0):  # Skip self-reference
                continue

            x, y, z = start_coord
            yield (x + dx, y + dy, z + dz)

    @staticmethod
    def neighbors_4d(start_coord: COORD4D) -> abc.Iterator[COORD4D]:
        """
        Yield coordinate quadruples for neighbors of the provided start coordinate.

        NOTE: The self reference `(0, 0, 0, 0)` is ignored.
        """
        for dx, dy, dz, dw in it.product((-1, 0, 1), repeat=4):
            if (dx, dy, dz, dw) == (0, 0, 0, 0):  # Skip self-reference
                continue

            x, y, z, w = start_coord
            yield (x + dx, y + dy, z + dz, w + dw)


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text()

    cube = ConwayCube(puzzle_input)
    cube.step_n(6)
    print(f"Part One: {cube.n_active} active cells")

    cube = ConwayCube(puzzle_input, ndims=4)
    cube.step_n(6)
    print(f"Part Two: {cube.n_active} active cells")
