from __future__ import annotations

import math
from collections import abc
from dataclasses import dataclass
from pathlib import Path

BOAT_ACCEL = 1  # mm/s^2


@dataclass
class RaceSpec:  # noqa: D101
    race_time: int
    distance_record: int

    @classmethod
    def from_race_document(cls, race_doc: str, ignore_spaces: bool = False) -> list[RaceSpec]:
        """
        Parse race parameters from the provided race document.

        The race document is assumed to be of the following form:

        ```
        Time:      7  15   30
        Distance:  9  40  200
        ```

        Where `Time:` describes the total duration of the race, in milliseconds, and `Distance:`
        describes the current distance record, in millimeters. All values are assumed to be
        integers.

        If `ignore_spaces` is `False`, each column corresponds to a specific race in the series. If
        `True`, the spaces are ignored and the race document is assumed to describe the parameters
        for a single race.
        """
        raw_times, raw_distances = (line.split(":")[-1].split() for line in race_doc.splitlines())

        times: abc.Iterable[int]
        distances: abc.Iterable[int]
        if ignore_spaces:
            # Keep as tuple so return statement stays consistent between flag states
            times = (int("".join(raw_times)),)
            distances = (int("".join(raw_distances)),)
        else:
            times = (int(v) for v in raw_times)
            distances = (int(v) for v in raw_distances)

        return [cls(time, distance_record) for time, distance_record in zip(times, distances)]


def winning_strategies(race_spec: RaceSpec) -> list[int]:
    """
    Determine all winning race strategies for the provided race parameters.

    Once the race begins, competitors can hold down a button to charge the boat. For each
    millisecond the button is held, the boat's speed will increase by one millimeter per second.
    Once the button is released, the boatimmediately begins traveling at this speed until the
    remaining time ends. Once released, the button cannot be pressed again.

    The resulting distance is considered winning if it exceeds the current course record.
    """
    winning_holds = []
    for hold_time in range(1, race_spec.race_time):
        travel_time = race_spec.race_time - hold_time
        travel_distance = (BOAT_ACCEL * hold_time) * travel_time
        if travel_distance > race_spec.distance_record:
            winning_holds.append(hold_time)

    return winning_holds


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    races = RaceSpec.from_race_document(puzzle_input)
    print(f"Part One: {math.prod(len(winning_strategies(race)) for race in races)}")

    long_race = RaceSpec.from_race_document(puzzle_input, ignore_spaces=True)[0]
    print(f"Part Two: {len(winning_strategies(long_race))}")
