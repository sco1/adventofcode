from __future__ import annotations

import typing as t
from pathlib import Path

# Number of display segments for 1, 4, 7, and 8 are unique
UNIQUE_LENGTHS = {2, 4, 3, 7}


class Signal(t.NamedTuple):  # noqa: D101
    # Patterns map to each one of the digits from 0-9, we just don't know which is which yet
    # We don't care about order & it makes part 2 simpler to use sets so we'll do it here
    signal_patterns: list[frozenset(str)]
    output_values: list[frozenset(str)]  # The 4 digit output value

    @classmethod
    def from_raw(cls, raw_patterns: list[str]) -> list[Signal]:
        """
        Split the signal patterns from our notes into their input & output components.

        Each note is assumed to have the input & output strings delimited by `|`. It is assumed that
        there are 9 input strings, corresponding to each of the 9 segments of the 7-segment display
        that has been randomly wired up. It is assumed that the inputs map to a single valid
        mapping. Outputs are assumed to be 4 strings, corresponding to a number to be displayed on
        the output 4-digit display.
        """
        parsed_signals = []
        for signal in raw_patterns:
            raw_in, raw_out = signal.split("|")
            parsed_signals.append(
                cls(
                    signal_patterns=[frozenset(segments) for segments in raw_in.strip().split()],
                    output_values=[frozenset(segments) for segments in raw_out.strip().split()],
                )
            )

        return parsed_signals


def n_simple_outputs(signal_patterns: list[Signal]) -> int:
    """Calculate the number of occurrences of the numbers `1`, `4`, `7`, or `8`."""
    # Since these digits have a unique number of component segments on the display, they can be
    # counted with a simple length check of the output strings
    n_simple = 0
    for signal in signal_patterns:
        n_simple += sum(len(segment) in UNIQUE_LENGTHS for segment in signal.output_values)

    return n_simple


def determine_output(input_signal: Signal) -> int:
    """Identify the correct segment mapping for the provided signal & return the displayed value."""
    digit_mapping = {}
    # Cache these for later
    six_segments = []
    five_segments = []
    # Since 1, 4, 7, and 8 are unique we start with their mapping
    for pattern in input_signal.signal_patterns:
        match len(pattern):
            case 2:
                digit_mapping[1] = pattern
            case 3:
                digit_mapping[7] = pattern
            case 4:
                digit_mapping[4] = pattern
            case 7:
                digit_mapping[8] = pattern
            case 6:
                six_segments.append(pattern)
            case 5:
                five_segments.append(pattern)
            case _:
                pass

    # Find the 6-segment numbers (0, 6, 9) next
    # Of these 3 numbers, 6 is the only one that doesn't share both segments of 1
    # Of the remaining 2 numbers (9, 0), 9 shares all segments of 4
    # This leaves 0
    for pattern in six_segments:
        if len(pattern & digit_mapping[1]) == 1:
            digit_mapping[6] = pattern
        elif len(pattern & digit_mapping[4]) == 4:
            digit_mapping[9] = pattern
        else:
            digit_mapping[0] = pattern

    # Finally, find the 5-segment numbers (2, 3, 5)
    # Of these 3 numbers, 6 is the only one that shares all segments of 5
    # Of the remaining 2 numbers (2, 3), 3 is the only one that shares both segments of 1
    # This leaves 2
    for pattern in five_segments:
        if len(pattern & digit_mapping[6]) == 5:
            digit_mapping[5] = pattern
        elif len(pattern & digit_mapping[1]) == 2:
            digit_mapping[3] = pattern
        else:
            digit_mapping[2] = pattern

    # Swap around the keys/values so we can look up by pattern instead of digit
    flipped = {v: k for k, v in digit_mapping.items()}
    out_components = [flipped[p] for p in input_signal.output_values]

    # Now we just have powers of 10
    max_power = len(out_components) - 1
    return sum(n * 10 ** (max_power - i) for i, n in enumerate(out_components))


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().splitlines()
    parsed_signals = Signal.from_raw(puzzle_input)

    print(f"Part One: {n_simple_outputs(parsed_signals)}")
    print(f"Part Two: {sum(determine_output(signal) for signal in parsed_signals)}")
