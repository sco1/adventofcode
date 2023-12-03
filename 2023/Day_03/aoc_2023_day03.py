from __future__ import annotations

import math
from collections import abc, deque
from dataclasses import dataclass
from pathlib import Path

from helpers.geometry import COORD, iter_neighbors


@dataclass(frozen=True)
class Number:  # noqa: D101
    val: int
    coords: set[COORD]

    def __hash__(self) -> int:
        return hash((self.val, tuple(sorted(self.coords))))

    def iter_neighbors(self, include_diagonal: bool = False) -> abc.Iterable[COORD]:  # noqa: D102
        seen = set(self.coords)
        for coord in self.coords:
            for neighbor in iter_neighbors(coord, include_diagonal=include_diagonal):
                if neighbor not in seen:
                    yield neighbor
                    seen.add(neighbor)

    @classmethod
    def from_buffer(cls, digit_buffer: list[tuple[int, str]], y: int) -> Number:  # noqa: D102
        val = int("".join(digit for _, digit in digit_buffer))
        locs = {(digit_x, y) for digit_x, _ in digit_buffer}

        return cls(val, locs)


def parse_schematic(schematic: str) -> tuple[list[Number], dict[COORD, str]]:
    """
    Parse the provided engine schematic into its component parts.

    The engine schematic contains a collection of symbols and numbers, with `.` denoting an empty
    space. The schematic is parsed for the locations of these values and returns the number & symbol
    locations separately.
    """
    numbers = []
    symbols = {}
    for y, line in enumerate(schematic.splitlines()):
        line_buffer = deque(line)
        digit_buffer: list[tuple[int, str]] = []
        x = 0
        while line_buffer:
            c = line_buffer.popleft()
            if c == ".":
                if digit_buffer:
                    numbers.append(Number.from_buffer(digit_buffer, y))
                    digit_buffer.clear()
            elif c.isdigit():
                digit_buffer.append((x, c))
            else:
                symbols[(x, y)] = c
                if digit_buffer:
                    numbers.append(Number.from_buffer(digit_buffer, y))
                    digit_buffer.clear()
            x += 1

        if digit_buffer:
            numbers.append(Number.from_buffer(digit_buffer, y))
            digit_buffer.clear()

    return numbers, symbols


def find_adjacent_parts(
    numbers: abc.Iterable[Number], symbol_locs: dict[COORD, str]
) -> abc.Iterable[int]:
    """
    Locate the part numbers for parts adjacent to a symbol in the provided schematic components.

    For example:
        ```
        467..114..
        ...*......
        ..35..633
        ......#...
        ```

    Would yield `467`, `35`, and `633`. Note that diagonals are considered.

    NOTE: Part numbers may be found in more than one location in the schematic & are emitted every
    time they are seen.
    """
    for num in numbers:
        for coord in num.iter_neighbors(include_diagonal=True):
            if coord in symbol_locs:
                yield num.val
                break


def find_gears(
    numbers: abc.Iterable[Number], symbol_locs: dict[COORD, str]
) -> abc.Iterable[tuple[int, int]]:
    """
    Identify gears from the provided schematic components.

    A gear is any `*` symbol that is adjacent to exactly two part numbers.
    """
    for loc, symbol in symbol_locs.items():
        if symbol == "*":
            adjacent_parts = set()
            for neighbor in iter_neighbors(loc, include_diagonal=True):
                for num in numbers:
                    if neighbor in num.coords:
                        adjacent_parts.add(num)
                        break

            if len(adjacent_parts) == 2:
                yield tuple(part.val for part in adjacent_parts)  # type: ignore[misc]


def sum_gear_ratios(gears: abc.Iterable[tuple[int, int]]) -> int:
    """
    Calculate the sum of the gear ratios of the provided gears.

    A gear's ratio is the product of the two part numbers making up the gear.
    """
    return sum(math.prod(gear) for gear in gears)


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    nums, syms = parse_schematic(puzzle_input)
    print(f"Part One: {sum(find_adjacent_parts(nums, syms))}")
    print(f"Part Two: {sum_gear_ratios(find_gears(nums, syms))}")
