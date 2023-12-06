from __future__ import annotations

import re
import typing as t
from collections import abc, deque
from dataclasses import dataclass, field
from pathlib import Path

import more_itertools as miter


@dataclass
class Mapping:
    """
    Represent an almanac's source-to-dest index mapping description.

    Instances of this class accept a source index, which will return the corresponding destination
    index if it exists in the range. It a corresponding value is not contained by this mapping,
    `None` is returned instead.
    """

    source: str
    dest: str

    source_start: int
    dest_start: int
    n_vals: int

    _source_range: range = field(init=False, repr=False)
    _offset: int = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._source_range = range(self.source_start, self.source_start + self.n_vals)
        self._offset = self.dest_start - self.source_start

    def __getitem__(self, source_loc: int) -> int | None:
        if source_loc not in self._source_range:
            return None

        return source_loc + self._offset

    @classmethod
    def from_str(cls, map_str: str, source: str, dest: str) -> Mapping:
        """
        Build a range mapping from the provided raw almanac information.

        Info is assumed to be of the form: `<destination start> <source start> <range length>`,
        where values are space-delimited integers.
        """
        dest_start, source_start, n_vals = (int(v) for v in map_str.split())
        return Mapping(
            source=source,
            dest=dest,
            source_start=source_start,
            dest_start=dest_start,
            n_vals=n_vals,
        )

    @classmethod
    def from_linebuffer(cls, buffer: list[str]) -> list[Mapping]:
        """
        Parse the provided buffer of raw almanac lines into a collection of mappings.

        The buffer is assumed be of the form:

        ```
        [
            "<source>-to-<destination> map:",
            "<destination start> <source start> <range length>",
            ...,
        ]
        ```

        Where the mapping range is of a form expected by `Mapping.from_string`.
        """
        mapping_header, *mappings = buffer
        source, dest = re.findall(r"(\w+)-to-(\w+)", mapping_header)[0]

        maps = []
        for map_str in mappings:
            maps.append(Mapping.from_str(map_str, source, dest))

        return maps


@dataclass
class SeedState:  # noqa: D101
    seed: int
    soil: int = -1
    fertilizer: int = -1
    water: int = -1
    light: int = -1
    temperature: int = -1
    humidity: int = -1
    location: int = -1

    def apply_mappings(self, mappings: abc.Iterable[Mapping]) -> None:
        """Apply the provided collection of <source>-<dest> mappings to the current seed state."""
        for mapping in mappings:
            source_idx = getattr(self, mapping.source)
            dest_idx = mapping[source_idx]

            target_val = getattr(self, mapping.dest)
            if dest_idx is None:
                if target_val == -1:
                    setattr(self, mapping.dest, source_idx)
                continue

            setattr(self, mapping.dest, dest_idx)


@t.overload
def parse_almanac(  # noqa: D103
    almanac: str, use_seed_range: t.Literal[True]
) -> tuple[list[range], list[Mapping]]:
    ...


@t.overload
def parse_almanac(  # noqa: D103
    almanac: str, use_seed_range: t.Literal[False] = False
) -> tuple[list[int], list[Mapping]]:
    ...


def parse_almanac(almanac, use_seed_range: t.Literal[True, False] = False):
    """
    Parse the provided almanac & return a collection of initial seed states.

    The almanac begins with a seed index line, followed by one or more newline delimited instruction
    maps. For example:

    ```
    seeds: <seed ids>

    <source>-to-<destination> map:
    <destination start> <source start> <range length>
    ```

    All numerical values are assumed to be positive, space delimited integers. Maps can have one or
    more range specifications.

    If `use_seed_range` is `False`, the seed index line is a simple index of seed locations. If the
    flag is `True`, then the seed line is assumed to be comprised of pairs that specify ranges of
    seed locations; the first number in each pair denotes the starting index and the second number
    denotes the length of the range.

    Each map describes how to convert the values from the source category into values in the
    destination category. Destination locations are provided as ranges, e.g. `50 98 3` maps to:
    `dest: (50, 51, 52), src: (98, 99, 100)`. Any source locations that aren't explicitly mapped
    correspond to the same destination location.
    """
    seed_spec, _, *map_spec = almanac.splitlines()  # Skip blank line between seeds & mappings

    maps = []
    queue = deque(map_spec)
    buffer = []
    while queue:
        line = queue.popleft()
        if line:
            buffer.append(line)
            continue

        maps.extend(Mapping.from_linebuffer(buffer))
        buffer.clear()

    # Clear buffer
    if buffer:
        maps.extend(Mapping.from_linebuffer(buffer))

    seed_nums = [int(v) for v in seed_spec.split(":")[-1].strip().split()]
    if use_seed_range:
        seeds = []
        for seed_start, range_len in miter.chunked(seed_nums, 2, strict=True):
            seeds.append(range(seed_start, seed_start + range_len))

        return seeds, maps
    else:
        return seed_nums, maps


def _iter_idx(seed_idx: abc.Iterable[int]) -> abc.Iterable[int]:  # noqa: D103
    for idx in seed_idx:
        yield idx


def _iter_ranges(seed_idx: abc.Iterable[range]) -> abc.Iterable[int]:
    """Iterate over the contained ranges and yield each value until exhausted."""
    for seed_range in seed_idx:
        for idx in seed_range:
            yield idx


def iter_seeds(
    seed_idx: list[int] | list[range], mappings: list[Mapping]
) -> abc.Iterable[SeedState]:
    """Iterate over the provided seed locations & apply the almanac mappings to each seed."""
    if isinstance(seed_idx[0], int):
        seed_nums = _iter_idx(seed_idx)  # type: ignore[arg-type]
    elif isinstance(seed_idx[0], range):
        seed_nums = _iter_ranges(seed_idx)  # type: ignore[arg-type]
    else:
        raise ValueError(f"Unsupported index type provided: {type(seed_idx[0])}")

    for n in seed_nums:
        s = SeedState(seed=n)
        s.apply_mappings(mappings)

        yield s


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    seed_idx, mappings = parse_almanac(puzzle_input)
    print(f"Part One: {min(seed.location for seed in iter_seeds(seed_idx, mappings))}")

    import time

    a = time.monotonic()
    seed_idx_range, mappings = parse_almanac(puzzle_input, use_seed_range=True)
    print(f"Part Two: {min(seed.location for seed in iter_seeds(seed_idx_range, mappings))}")
    b = time.monotonic()
    print("Elapsed seconds: ", b - a)
