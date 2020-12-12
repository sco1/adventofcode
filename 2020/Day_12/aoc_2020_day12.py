import typing as t
from collections import deque
from pathlib import Path


class AdventFerry:  # noqa: D101
    x_pos: int  # East positive, West negative
    y_pos: int  # North positive, South negative
    compass: t.Deque[str]  # Contains the 4 cardinal directions & rotates to give direction

    waypoint_mode: bool
    waypoint_x: int  # East positive, West negative
    waypoint_y: int  # North positive, South negative

    directions: list[tuple[str, int]]
    _instruction_mapping: dict[str, t.Callable]

    def __init__(self, raw_directions: str, facing: str = "E", waypoint_mode: bool = False) -> None:
        self.set_instruction_mapping(waypoint_mode)
        self.directions = self.parse_directions(raw_directions)

        self.x_pos = 0
        self.y_pos = 0
        self.calibrate_compass(facing)

        if waypoint_mode:
            self.waypoint_x = 10
            self.waypoint_y = 1

    def set_instruction_mapping(self, waypoint_mode: bool) -> None:
        """
        Map the instruction set based on the provided steering mode flag.

        If the ship is in Waypoint Mode, the instruction set manipulates the ship's steering
        waypoint, driving it to the waypoint whe the `"F"` instruction is encountered. Otherwise,
        the instruction set manipulates the ship directly.
        """
        if waypoint_mode:
            self._instruction_mapping = {
                "N": lambda y: self.move_waypoint_y(y),
                "S": lambda y: self.move_waypoint_y(-y),
                "E": lambda x: self.move_waypoint_x(x),
                "W": lambda x: self.move_waypoint_x(-x),
                "L": lambda d: self.rotate_waypoint(-d),
                "R": lambda d: self.rotate_waypoint(d),
                "F": lambda n: self.move_to_waypoint(n),
            }
        else:
            self._instruction_mapping = {
                "N": lambda y: self.move_y(y),
                "S": lambda y: self.move_y(-y),
                "E": lambda x: self.move_x(x),
                "W": lambda x: self.move_x(-x),
                "L": lambda d: self.rotate(-d),
                "R": lambda d: self.rotate(d),
                "F": lambda n: self.move_forward(n),
            }

    def calibrate_compass(self, facing: str) -> None:
        """
        Instantiate & reset the ship's compass to the provided initial orientation.

        Initial orientation is assumed to be a cardinal direction: "N", "E", "S", or "W".
        """
        self.compass = deque(("N", "E", "S", "W"), maxlen=4)
        if facing not in self.compass:
            raise ValueError(f"Unknown starting direction: '{facing}'")

        while self.compass[0] != facing:
            self.compass.rotate()

    def parse_directions(self, raw_directions: str) -> list[tuple[str, int]]:
        """
        Parse the provided raw instruction set into a list of instructions.

        Instructions are parsed into (Callable, value) tuples, which the ship executes later on.
        """
        directions = []
        for line in raw_directions.splitlines():
            instruction = line[0]
            val = int(line[1:])

            directions.append((self._instruction_mapping[instruction], val))

        return directions

    def distance_from_start(self, start: tuple[int, int] = (0, 0)) -> int:
        """Calculate the Manhattan distance from the start point to the ship's current location."""
        dx = abs(self.x_pos - start[0])
        dy = abs(self.y_pos - start[1])

        return dx + dy

    def move_x(self, val: int) -> None:
        """Shift the ship's x coordinate by the provided value."""
        self.x_pos += val

    def move_y(self, val: int) -> None:
        """Shift the ship's y coordinate by the provided value."""
        self.y_pos += val

    def move_forward(self, val: int) -> None:
        """Move the ship by the provided value in the direction it's currently facing."""
        self._instruction_mapping[self.compass[0]](val)

    def rotate(self, val: int) -> None:
        """
        Rotate the ship's orientation by the provided value.

        NOTE: Input values are assumed to be dregrees & in whole multiples of 90.
        """
        # Negate val here since the deque rotation is opposite of what we want
        # e.g. Turning right is a positive degree rotation, but rotating the deque right would be a
        # left turn
        n_steps = -val // 90
        self.compass.rotate(n_steps)

    def move_waypoint_x(self, val: int) -> None:
        """Shift the waypoint's x coordinate by the provided value."""
        self.waypoint_x += val

    def move_waypoint_y(self, val: int) -> None:
        """Shift the waypoint's y coordinate by the provided value."""
        self.waypoint_y += val

    def move_to_waypoint(self, val: int) -> None:
        """Drive the ship from its current position to the waypoint; repeat `val` times."""
        self.x_pos += self.waypoint_x * val
        self.y_pos += self.waypoint_y * val

    def rotate_waypoint(self, val: int) -> None:
        """
        Rotate the waypoint around the ship by the provided value.

        NOTE: Input values are assumed to be dregrees & in whole multiples of 90.
        """
        # Realistically we would just use trig here, but since we have some simplifying assumptions
        # let's take a different approach so we can avoid needing floating point math
        #
        # Rotation by 90 degrees swaps the x,y components & negates one of them, depending on the
        # direction of rotation
        # e.g. rotating (3, 1) 90 degrees clockwise gives us (1, -3)
        #      rotating (3, 1) 90 degrees counter-clockwise gives us (-1, 3)
        n_steps = abs(val // 90) % 4  # Assuming 90 degree rotations we get 4 before we rotate back
        for _ in range(n_steps):
            self.waypoint_x, self.waypoint_y = self.waypoint_y, self.waypoint_x
            if val < 0:
                self.waypoint_x *= -1
            else:
                self.waypoint_y *= -1

    def run(self) -> None:
        """Step through the parsed directions until completion."""
        for step, val in self.directions:
            step(val)


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text()

    advent_cruise = AdventFerry(puzzle_input)
    advent_cruise.run()
    print(f"Part 1: {advent_cruise.distance_from_start()} bananas from starting location")

    advent_cruise = AdventFerry(puzzle_input, waypoint_mode=True)
    advent_cruise.run()
    print(f"Part 2: {advent_cruise.distance_from_start()} bananas from starting location")
