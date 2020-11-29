import re
from pathlib import Path


class Reindeer:
    """Represent a reindeer participating in the Reindeer Race."""

    _pattern = re.compile(
        r"(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds"
    )

    elapsed_seconds: int
    distance: int
    is_resting: bool
    points: int
    _flight_end: int  # Last timestamp for current flight segment
    _rest_end: int  # Last timestamp for current rest segment

    def __init__(self, name: str, speed: int, flight_time: int, rest_time: int):
        self.name = name
        self.speed = speed
        self.flight_time = flight_time
        self.rest_time = rest_time
        self.reset()

    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"{self.name!r}, {self.speed!r}, {self.flight_time!r}, {self.rest_time!r}"
            ")"
        )

    @classmethod
    def from_puzzle_input(cls, puzzle_input_line: str):
        """
        Instantiate a Reindeer instance from the provided puzzle input line.

        e.g. "Rudolph can fly 22 km/s for 8 seconds, but then must rest for 165 seconds."
        """
        name, speed, flight_time, rest_time = cls._pattern.search(puzzle_input_line).groups()
        return cls(name, int(speed), int(flight_time), int(rest_time))

    def reset(self) -> None:
        """Restart the reindeer to its initial state."""
        self.elapsed_seconds = 0
        self.distance = 0
        self.is_resting = False
        self.points = 0
        self._rest_end = None
        self._flight_end = self.flight_time - 1

    def step(self) -> None:
        """Advance the reindeer's position by 1 second & update its state."""
        if self.is_resting:
            if self.elapsed_seconds == self._rest_end:
                # Reindeer will stop resting this timestamp
                self.is_resting = False
                self._flight_end = self.elapsed_seconds + self.flight_time
        else:
            self.distance += self.speed
            if self._flight_end == self.elapsed_seconds:
                # Reindeer will rest after this timestamp
                self.is_resting = True
                self._rest_end = self.elapsed_seconds + self.rest_time

        self.elapsed_seconds += 1


class ReindeerRace:
    """Container for running the reindeer race simulation."""

    elapsed_seconds: int
    distance_leader: Reindeer
    points_leader: Reindeer

    def __init__(self, reindeer: list[Reindeer]):
        self.reindeer = reindeer
        self.restart()

    def restart(self) -> None:
        """
        Restart the race & leaderboards.

        For initial seeding, the first parsed reindeer is used for the initial leader positions
        """
        self.elapsed_seconds = 0
        self.points_leader = self.reindeer[0]
        self.distance_leader = self.reindeer[0]
        for deer in self.reindeer:
            deer.reset()

    def step_n(self, n_steps: int) -> None:
        """Advance the race simulation by the provided number of seconds."""
        for _ in range(n_steps):
            for deer in self.reindeer:
                deer.step()
                if deer.distance > self.distance_leader.distance:
                    self.distance_leader = deer

            self.award_points()

            self.elapsed_seconds += 1

    def award_points(self) -> None:
        """
        Award a point to the reindeer leading the race & update points leader, if necessary.

        In the event of a tie, all tied reindeer are awarded a point.
        """
        for deer in self.reindeer:
            if deer.distance == self.distance_leader.distance:
                deer.points += 1

            if deer.points > self.points_leader.points:
                self.points_leader = deer


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().splitlines()

    reindeer = [Reindeer.from_puzzle_input(line) for line in puzzle_input]
    race = ReindeerRace(reindeer)
    race.step_n(2503)

    print(
        (
            f"Distance leader after {race.elapsed_seconds} seconds is {race.distance_leader.name}! "
            f"They have traveled {race.distance_leader.distance} km."
        )
    )

    print(
        (
            f"Points leader after {race.elapsed_seconds} seconds is {race.points_leader.name}! "
            f"They have {race.points_leader.points} points."
        )
    )
