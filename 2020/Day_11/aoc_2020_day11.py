import itertools as it
from collections import abc
from pathlib import Path


COORD = tuple[int, int]


class SeatMap:  # noqa: D101
    def __init__(self, raw_chart: str) -> None:
        self._step = 0
        self.seat_map, self._length, self._width = self.parse_chart(raw_chart)

    def __str__(self):
        lines = []
        for row in range(self._length):
            line = [self.seat_map.get((row, col), ".") for col in range(self._width)]
            lines.append("".join(line))

        return "\n".join(lines)

    def n_occupied(self) -> int:
        """Count the number of occupied seats in the seat map."""
        return sum((seat == "#") for seat in self.seat_map.values())

    def gen_neighbor_idx(self, start_coord: COORD) -> abc.Iterator[COORD]:
        """Yield coordinate pairs for the valid neighbors of the provided start coordinates."""
        x, y = start_coord
        for dx, dy in it.product([-1, 0, 1], repeat=2):
            if (dx, dy) == (0, 0):  # Skip self-reference
                continue

            # Don't yield a coordinate pair if it's not in the seat map
            # i.e. it's the floor or it's outside of the ferry
            neighbor_coord = (x + dx, y + dy)
            if neighbor_coord in self.seat_map:
                yield neighbor_coord

    def step_boarding(self) -> None:
        """
        Run one timestep of the boarding process according to the provided boarding rules.

        * If a seat is empty (`"L"`) and there are no occupied seats adjacent to it, the seat
        becomes occupied.
        * If a seat is occupied (`"#"`) and 4 or more seats adjacent to it are also occupied, the
        seat becomes empty.
        * Otherwise, the seat's state does not change.
        """
        self._step += 1

        new_map = {}
        for seat_coord, seat in self.seat_map.items():
            # Count the occupied neighbors so we know if we need to fill the seat
            n_occupied_neighbors = 0
            for neighbor_coord in self.gen_neighbor_idx(seat_coord):
                if self.seat_map[neighbor_coord] == "#":
                    n_occupied_neighbors += 1

            if seat == "L":
                # Empty seat, fill if there are no occupied seats adjacent to it
                new_map[seat_coord] = "#" if n_occupied_neighbors == 0 else "L"
            elif seat == "#":
                # Occupied seat, empty if four or more adjacent seats are occupied
                new_map[seat_coord] = "L" if n_occupied_neighbors >= 4 else "#"

        self.seat_map = new_map

    def board_until_stable(self) -> None:
        """Run the boarding process until the seat map stabilizes (stops changing)."""
        while True:
            old_map = self.seat_map

            self.step_boarding()
            if self.seat_map == old_map:
                return

    @staticmethod
    def parse_chart(raw_chart: str) -> tuple[dict[COORD, str], int, int]:
        """
        Parse the provided raw seating chart into the internal seat map representation.

        For the provided seat map input:
            * `"L"` represents an empty seat
            * `"#"` represents an occupied seat
            * `"."` represents the floor

        The seat map is parsed into a dictionary of coordinate pair, seat key, value pairs. Floor
        coordinates are not included in the parsed seat map.

        The length and width of the ferry is also returned.
        """
        seat_map = {}
        for row_idx, row in enumerate(raw_chart.splitlines()):
            for col_idx, symbol in enumerate(row):
                if symbol in "L#":
                    seat_map[(row_idx, col_idx)] = symbol

        length = row_idx + 1
        width = row_idx + 1
        return seat_map, length, width


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text()

    seat_map = SeatMap(puzzle_input)
    seat_map.board_until_stable()
    print(f"Part One: {seat_map.n_occupied()} occupied seats")
