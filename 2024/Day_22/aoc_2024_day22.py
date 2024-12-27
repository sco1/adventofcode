from collections import abc
from pathlib import Path


def mix(secret: int, val: int) -> int:
    """
    Mix the provided value into the scret number.

    To mix a value into the secret number, calculate the bitwise XOR of the given value and the
    secret number.
    """
    return val ^ secret


def prune(secret: int) -> int:
    """
    Prune the secret number.

    To prune the secret number, calculate the value of the secret number modulo `16777216`.
    """
    return secret % 16_777_216


def evolve_secret(secret: int) -> abc.Generator[int, None, None]:
    """
    Generate the next secret number based on the provided starting seed.

    Each evolution of the secret number is calculated using the following steps:
        * Multiply the secret number by `64`. Then, mix this result into the secret number. Finally,
        prune the secret number.
        * Divide the secret number by `32`. Round the result down to the nearest integer. Then, mix
        this result into the secret number. Finally, prune the secret number.
        * Multiply the secret number by `2048`. Then, mix this result into the secret number.
        Finally, prune the secret number.
    """
    while True:
        secret = prune(mix(secret, secret * 64))
        secret = prune(mix(secret, secret // 32))
        secret = prune(mix(secret, secret * 2048))
        yield secret


def nth_secret(seed: int, n: int = 2000) -> int:
    """Calculate the nth secret number based on the provided starting seed."""
    sn = evolve_secret(seed)
    for _ in range(n - 1):
        next(sn)

    return next(sn)


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    market_seeds = [int(n) for n in puzzle_input.splitlines()]

    print(f"Part One: {sum(nth_secret(seed) for seed in market_seeds)}")
    print(f"Part Two: {...}")
