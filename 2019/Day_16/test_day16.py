import pytest

# Test cases are provided as (input, number of phases, truth output)
PART_ONE = [
    (
        "12345678",
        4,
        "01029498",
    ),
    ("80871224585914546619083218645595", 100, "24176176"),
    ("19617804207202209144916044189917", 100, "73745418"),
    ("69317163492948606335995924319873", 100, "52432133"),
]

# Test cases are provided as (input, truth output)
# Note that the input will be repeated 10,000 times to create the input signal
PART_TWO = [
    ("03036732577212944063491565474664", "84462026"),
    ("02935109699940807407585447034323", "78725270"),
    ("03081770884921959731165446850517", "53553731"),
]


@pytest.mark.parametrize("input, n_phases, truth_output", PART_ONE)
def test_part_one(input: str, n_phases: int, truth_output: str) -> None:
    """Test for correct FFT calculation after the specified number of phases."""
    raise NotImplementedError


@pytest.mark.parametrize("input, truth_message", PART_TWO)
def test_part_two(input: str, truth_output: str) -> None:
    """Test for correct decoding of the message in the input signal."""
    raise NotImplementedError
