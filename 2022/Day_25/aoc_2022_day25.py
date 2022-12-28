from pathlib import Path

SNAF_MAP = {
    "=": -2,
    "-": -1,
    "0": 0,
    "1": 1,
    "2": 2,
}

DEC_MAP = {
    -2: "=",
    -1: "-",
    0: "0",
    1: "1",
    2: "2",
}


def dec2sanfu(in_dec: int) -> str:  # noqa: D103
    out_snafu = []
    while in_dec > 0:
        # Since we're shifted by 2, if our remainder is 3 or 4 then we get back around to -1 or -2
        # by carrying forward from the next power of 5. We can do this same shift before division
        # so we don't have to deal with a conditional
        in_dec, mod = divmod(in_dec + 2, 5)
        out_snafu.append(DEC_MAP[mod - 2])  # Rotate back to correct index

    return "".join(reversed(out_snafu))


def snafu2dec(in_snafu: str) -> int:  # noqa: D103
    out_val = 0
    for idx, c in enumerate(reversed(in_snafu)):
        out_val += (5**idx) * SNAF_MAP[c]

    return out_val


def calculate_fuel_requirement(requirements: str) -> tuple[str, int]:
    """
    Calculate the total fuel requirements for all of the provided hot air balloons.

    Requirements are assumed to be provided in Special Numeral-Analogue Fuel Units (SNAFU), which
    uses powers of five and digits `=-012`, where `=` represents `-2` and `-` represents `-1`.

    Fuel requirements are output as a SNAFU, decimal tuple.
    """
    total_fuel = sum(snafu2dec(line) for line in requirements.splitlines())
    total_fuel_snafu = dec2sanfu(total_fuel)

    return total_fuel_snafu, total_fuel


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text()

    snaf, dec = calculate_fuel_requirement(puzzle_input)
    print(f"Part One: {snaf}")
