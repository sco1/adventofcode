from __future__ import annotations

import math
import re
from pathlib import Path
from typing import List

from more_itertools import distinct_combinations


def lcm(a: int, b: int) -> int:
    """Calculate the least common multiple of two integers."""
    return abs(a * b) // math.gcd(a, b)


class Moon:
    """Represent a moon of Jupyter."""

    # Moon coordinates are provided as "<x=-1, y=0, z=2>"
    COORD_EXP = r"<x=(.+), y=(.+), z=(.+)>"

    def __init__(self, x_init: int, y_init: int, z_init: int):
        self.x = x_init
        self.y = y_init
        self.z = z_init

        self.v_x = self.v_y = self.v_z = 0

    @property
    def pe(self) -> int:
        """
        Calculate the Moon's potential energy.

        Defined as the sum of the absolute values of its x,y,z coordinates.
        """
        return abs(self.x) + abs(self.y) + abs(self.z)

    @property
    def ke(self) -> int:
        """
        Calculate the Moon's kinetic energy.

        Defined as the sum of the absolute values of its x,y,z velocities.
        """
        return abs(self.v_x) + abs(self.v_y) + abs(self.v_z)

    @property
    def total_energy(self) -> int:
        """Calculate the Moon's total energy, calculated as Kinetic + Potential energy."""
        return self.pe * self.ke

    def apply_grav(self, other: Moon) -> None:
        """
        Apply gravitational acceleration to the pair of Moon instances.

        The velocity of each moon, on each axis, changes by exactly +1 or -1 to pull the moons
        together. If the positions on a given axis are the same, the velocity on that axis does not
        change.
        """
        for velocity_component, position_component in (
            ("v_x", "x"),
            ("v_y", "y"),
            ("v_z", "z"),
        ):
            self_pos = getattr(self, position_component)
            self_vel = getattr(self, velocity_component)
            other_pos = getattr(other, position_component)
            other_vel = getattr(other, velocity_component)
            if self_pos > other_pos:
                setattr(self, velocity_component, self_vel - 1)
                setattr(other, velocity_component, other_vel + 1)
            elif self_pos < other_pos:
                setattr(self, velocity_component, self_vel + 1)
                setattr(other, velocity_component, other_vel - 1)

    def step_velocity(self) -> None:
        """Increment each position component by its current respective velocity component."""
        self.x += self.v_x
        self.y += self.v_y
        self.z += self.v_z

    @classmethod
    def from_string(cls, coords: str) -> Moon:
        """Build a Moon instance from the provided coordinate string, as '<x=1, y=2, z=3>'."""
        x, y, z = (int(coord) for coord in re.findall(cls.COORD_EXP, coords)[0])
        return cls(x, y, z)

    def __str__(self):
        return (
            f"({self.x}, {self.y}, {self.z}) <{self.v_x}, {self.v_y}, {self.v_z}>: "
            f"PE={self.pe}, KE={self.ke}"
        )

    def _debug_str(self) -> str:
        """Generate a system state string that matches AOC's problem statement format."""
        return (
            f"pos=<x={self.x:5}, y={self.y:5}, z={self.z:5}>, "
            f"vel=<x={self.v_x:5}, y={self.v_y:5}, z={self.v_z:5}>, "
            f"PE={self.pe:4}, KE={self.ke:4}, TE={self.total_energy:6}"
        )


class Planet:
    """Represent a planet and its collection of Moons."""

    def __init__(self, moons: List[Moon]):
        self.moons = moons
        self._timestep = 0

        self._x_states = set()
        self._y_states = set()
        self._z_states = set()
        self.x_repeat = self.y_repeat = self.z_repeat = None
        self.save_state()

    @property
    def pe(self) -> int:
        """Calculate the sum of the potential energy for all moons in orbit."""
        return sum(moon.pe for moon in self.moons)

    @property
    def ke(self) -> int:
        """Calculate the sum of the kinetic energy for all moons in orbit."""
        return sum(moon.ke for moon in self.moons)

    @property
    def total_energy(self) -> int:
        """Calculate the total energy for all moons in orbit."""
        return sum(moon.total_energy for moon in self.moons)

    @classmethod
    def from_moon_map(cls, moon_map: List[str]) -> Planet:
        """
        Build a Planet instance from the moon coordinates provided by `moon_map`.

        `moon_map` is assumed to be a list of strings of the form "<x=1, y=2, z=3>"
        """
        return cls([Moon.from_string(moon_coords) for moon_coords in moon_map])

    def save_state(self) -> None:
        """Hash & store the orbital state components."""
        # Only calculate component hashes if we haven't already seen a repeat yet
        if not self.x_repeat:
            x_hash = hash(tuple((moon.x, moon.v_x) for moon in self.moons))
            if x_hash in self._x_states:
                self.x_repeat = self._timestep
            else:
                self._x_states.add(x_hash)

        if not self.y_repeat:
            y_hash = hash(tuple((moon.y, moon.v_y) for moon in self.moons))
            if y_hash in self._y_states:
                self.y_repeat = self._timestep
            else:
                self._y_states.add(y_hash)

        if not self.z_repeat:
            z_hash = hash(tuple((moon.z, moon.v_z) for moon in self.moons))
            if z_hash in self._z_states:
                self.z_repeat = self._timestep
            else:
                self._z_states.add(z_hash)

    def advance_sim(self, n_steps: int) -> None:
        """Advance the simulation `n_steps` into the future."""
        for _ in range(n_steps):
            for moon_a, moon_b in distinct_combinations(self.moons, 2):
                moon_a.apply_grav(moon_b)

            for moon in self.moons:
                moon.step_velocity()

            self._timestep += 1
            self.save_state()

    def find_repeat(self) -> int:
        """
        Determine the number of simulation steps until the orbital state repeats.

        Iterate the simulation until a repeat position,velocity pair is found for each axis
        component, establishing the cycle for the axis. Once all 3 cycles are determined, we can use
        lcm to find the total number of steps necessary to reach an orbital state that's been seen
        """
        while not all((self.x_repeat, self.y_repeat, self.z_repeat)):
            self.advance_sim(1)

        return lcm(lcm(self.x_repeat, self.y_repeat), self.z_repeat)

    def _debug_str(self) -> str:
        """Generate a system state string that matches AOC's problem statement format."""
        moon_strs = "\n".join(moon._debug_str() for moon in self.moons)
        return f"{moon_strs}\n" f"PE={self.pe}, KE={self.ke}, TE={self.total_energy}"


if __name__ == "__main__":
    puzzle_input = Path("./puzzle_input.txt")

    with puzzle_input.open("r") as f:
        moon_map = [line.strip() for line in f.readlines()]

    # Part 1
    jupiter = Planet.from_moon_map(moon_map)
    jupiter.advance_sim(1000)
    print(jupiter.total_energy)

    # Part 2
    jupiter = Planet.from_moon_map(moon_map)
    print(jupiter.find_repeat())
