from __future__ import annotations

import itertools
from collections import abc, defaultdict
from dataclasses import dataclass
from pathlib import Path

from helpers.geometry import COORD
from helpers.parsing import parse_hashed_map


def hash_to_tumbler(hash_coords: set[COORD]) -> tuple[int, ...]:
    """
    Calculate pin heights for each tumbler based on the provided schematic hashes.

    NOTE: Each schematic has is assumed to contain one complete row of hashes (top for locks, bottom
    for keys), and pin heights are determined relative to this row.

    For example, this lock has pin heights of `(0, 5, 3, 4, 3)`

    ```
    #####
    .####
    .####
    .####
    .#.#.
    .#...
    .....
    ```
    """
    heights: dict[int, int] = defaultdict(int)
    for c in hash_coords:
        heights[c[0]] += 1

    pins = tuple(heights[col] - 1 for col in sorted(heights.keys()))
    return pins


def fits(key: Key, lock: Lock) -> bool:
    """
    Check that the lock & key combination fits together.

    A fit is deemed valid if the lock & key do not overlap any pins when combined.
    """
    if key.n_tumblers != lock.n_tumblers:
        raise ValueError(f"Tumbler mismatch. Lock: {lock.n_tumblers}, Key: {key.n_tumblers}")

    return all(sum(n) <= lock.n_pins for n in zip(lock.pins, key.pins))


@dataclass(slots=True)
class Lock:  # noqa: D101
    pins: tuple[int, ...]
    n_pins: int = 5

    @property
    def n_tumblers(self) -> int:  # noqa: D102
        return len(self.pins)

    @classmethod
    def from_raw(cls, raw_schematic: str) -> Lock:
        """
        Parse the lock parameters from the provided schematic.

        Pin schematics are assumed to be a grid of ASCII characters denoting pins (`#`) and empty
        space (`.`). Lock schematics are assumed to contain a top row filled entirely with `#`.
        """
        tumbler_coords = parse_hashed_map(raw_schematic)
        return cls(pins=hash_to_tumbler(tumbler_coords))


@dataclass(slots=True)
class Key:  # noqa: D101
    pins: tuple[int, ...]

    @property
    def n_tumblers(self) -> int:  # noqa: D102
        return len(self.pins)

    @classmethod
    def from_raw(cls, raw_schematic: str) -> Key:
        """
        Parse the key parameters from the provided schematic.

        Pin schematics are assumed to be a grid of ASCII characters denoting pins (`#`) and empty
        space (`.`). Key schematics are assumed to contain a bottom row filled entirely with `#`.
        """
        tumbler_coords = parse_hashed_map(raw_schematic)
        return cls(pins=hash_to_tumbler(tumbler_coords))


def is_lock(raw_schematic: str) -> bool:  # noqa: D103
    split_schematic = raw_schematic.splitlines()
    return all(c == "#" for c in split_schematic[0])


def parse_schematics(raw_schematics: str) -> tuple[list[Lock], list[Key]]:
    """
    Parse the provided lock & key schematics into their equivalent `Lock` and `Key` instances.

    Pin schematics are assumed to be a grid of ASCII characters denoting pins (`#`) and empty
    space (`.`). Lock schematics are assumed to contain a top row filled entirely with `#`, and key
    schematics are assumed to contain a bottom row filled entirely with `#`.
    """
    locks = []
    keys = []
    for schematic in raw_schematics.split("\n\n"):
        if is_lock(schematic):
            locks.append(Lock.from_raw(schematic))
        else:
            keys.append(Key.from_raw(schematic))

    return locks, keys


def n_fits(locks: abc.Iterable[Lock], keys: abc.Iterable[Key]) -> int:
    """
    Check every lock & key combination and count the number of valid fits.

    A fit is deemed valid if the lock & key do not overlap any pins when combined.
    """
    return sum(fits(lock=lock, key=key) for lock, key in itertools.product(locks, keys))


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    locks, keys = parse_schematics(puzzle_input)

    print(f"Part One: {n_fits(locks, keys)}")
    print(f"Part Two: {...}")
