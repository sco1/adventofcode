import itertools
import operator
import typing as t
from pathlib import Path

from intcode.machine import IntcodeMachine

SEQUENCE_T: t.TypeAlias = tuple[int, ...]


def run_controllers(program: str, phase_sequence: SEQUENCE_T) -> int:
    """
    Run a series of Amplifier Controllers with the given phase sequence.

    Each controller is initialized with its respective phase from the phase sequence and is assumed
    to run until completion and output a signal that is fed as a second input to the next controller
    in the series. The first controller is fed an input signal of `0`.
    """
    signal = "0"  # Start signal to first controller
    for phase in phase_sequence:
        im = IntcodeMachine(program, stdin=(str(phase), signal))
        im.run()
        signal = im.stdout.popleft()

    return int(signal)


def find_max_thruster_setting(program: str, n_amps: int = 5) -> tuple[int, SEQUENCE_T]:
    """
    Calculate the phase sequence that provides the maximum thrust signal.

    Amplifier controllers are assumed to run in series using phase settings defined as integers from
    `0` to `n_amps - 1`.
    """
    max_thruster: tuple[int, SEQUENCE_T] = (-1, ())
    for phase_sequence in itertools.permutations(range(n_amps)):
        thrust = run_controllers(program, phase_sequence)
        max_thruster = max(max_thruster, (thrust, phase_sequence), key=operator.itemgetter(0))

    return max_thruster


def run_looped_controllers(program: str, phase_sequence: SEQUENCE_T) -> int:
    """
    Run a series of Amplifier Controllers with the given phase sequence.

    Each controller is initialized with its respective phase from the phase sequence and is assumed
    to run until completion and output a signal that is fed as a second input to the next controller
    in the series. The first controller is fed an input signal of `0`.
    """
    ...


def find_max_thruster_setting_feedback(program: str, n_amps: int = 5) -> tuple[int, SEQUENCE_T]:
    """
    Calculate the phase sequence that provides the maximum thrust signal.

    Amplifier controllers are assumed to be looped, so the final amplifier feeds its signal back to
    the initial amplifier. Amplifiers send signals to the next amplifier they are connected to and
    will repeatedly take input and produce output until the program is halted.

    Controllers uer phase settings defined as integers from `5` to `5 + n_amps - 1`.
    """
    max_thruster: tuple[int, SEQUENCE_T] = (-1, ())
    for phase_sequence in itertools.permutations(range(5, 5 + n_amps)):
        thrust = run_looped_controllers(program, phase_sequence)
        max_thruster = max(max_thruster, (thrust, phase_sequence), key=operator.itemgetter(0))

    return max_thruster


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    print(f"Part One: {find_max_thruster_setting(puzzle_input)[0]}")
    print(f"Part Two: {find_max_thruster_setting_feedback(puzzle_input)[0]}")
