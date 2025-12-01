import typing as t
from collections import abc
from enum import StrEnum
from pathlib import Path


class Direction(StrEnum):  # noqa: D101
    LEFT = "L"
    RIGHT = "R"


class Rotation(t.NamedTuple):  # noqa: D101
    direction: Direction
    n: int

    @classmethod
    def from_str(cls, in_str: str) -> t.Self:
        """
        Parse a rotation instruction from its raw form.

        Rotations are assumed to be of the form: `"<direction><magnitude>"`, e.g. `"L69"` or `"R1"`
        """
        dir_str, mag = in_str[0], in_str[1:]
        return cls(direction=Direction(dir_str), n=int(mag))


def rotate_dial(start: int, rotation: Rotation, dial_size: int = 100) -> int:
    """Determine the dial's end point when rotating from `start` using the given instruction."""
    if rotation.direction == Direction.LEFT:
        end = start - rotation.n
    else:
        end = start + rotation.n

    return end % dial_size


def find_password(
    rotations: abc.Iterable[Rotation],
    start: int = 50,
    dial_size: int = 100,
    include_passing: bool = False,
) -> int:
    """
    Determine the password for the North Pole's secret entrance given the provided instructions.

    The provided instructions denote a sequence of dial rotations indicating how to open the safe.
    However, the safe is a decoy and the password is determined as follows:
        * If `include_passing` is `False`, the password is the number of times the dial points to
        `0` after any rotation in the sequence.
        * If `include_passing` is `True`, the password is the number of times the dial points to `0`
        after any rotation in the sequence, plus the number of times the dial passes `0` during a
        rotation. This is also known as Password Method `0x434C49434B`.
    """
    n_zeros = 0
    for rot in rotations:
        if include_passing:
            n_zeros += rot.n // dial_size  # Full rotations
            shift = rot.n % dial_size  # Actual digit shift

            # Check whether the described rotation crosses 0
            # Since we are still counting landing at 0 after this block, it is not included in the
            # crossing check
            crossed = ((rot.direction == Direction.LEFT) and (shift > start)) or (
                (rot.direction == Direction.RIGHT) and (shift + start > dial_size)
            )

            # Make sure that a start position of 0 isn't counted as a crossing
            if (start != 0) and crossed:
                n_zeros += 1

        start = rotate_dial(start, rot)
        if start == 0:
            n_zeros += 1

    return n_zeros


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    ROTATIONS = [Rotation.from_str(s) for s in puzzle_input.splitlines()]

    print(f"Part One: {find_password(ROTATIONS)}")
    print(f"Part Two: {find_password(ROTATIONS, include_passing=True)}")
