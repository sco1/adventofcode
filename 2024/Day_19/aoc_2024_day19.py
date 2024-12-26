from functools import cache
from pathlib import Path


def parse_onsen_station(raw_state: str) -> tuple[tuple[str, ...], list[str]]:
    """
    Parse the Onsen table into its components.

    The Onsen's table is assumed to contain a collection of towels with a pattern of colored
    stripes along with a list of designs to display, where each design is a sequence of stripe
    colors.

    Available towels and target designs are assumed to be delimited by a blank line, where available
    towels are provided as a comma separated list of strings and target designs are provided as
    newline-delimited strings, e.g.:

    ```
    r, wr, b, g, bwu, rb, gb, br

    brwrr
    bggr
    gbbr
    rrbgbr
    ubwu
    bwurrg
    brgr
    bbrgwb
    ```
    """
    raw_towels, raw_patterns = raw_state.split("\n\n")
    towels = tuple(t.strip() for t in raw_towels.split(","))

    return towels, raw_patterns.splitlines()


@cache
def is_possible(towels: tuple[str, ...], pattern: str) -> bool:
    """
    Determine if the specified display pattern can be built using the available towel patterns.

    It is assumed that the onsen has essentially unlimited towel patterns available to use for
    making each design. Towels cannot be reversed, as this would make the onsen logo face the wrong
    way and that is unacceptable.
    """
    # A surprisingly straightforward recursion; as we traverse the design first check whether the
    # target subpattern is empty, indicating that we've matched the entire pattern. Otherwise we
    # continue on slicing and seeing if any of our available towels match the beginning of the
    # subpattern
    return not pattern or any(
        is_possible(towels, pattern[len(t) :]) for t in towels if pattern.startswith(t)
    )


def count_possible(towels: tuple[str, ...], patterns: list[str]) -> int:
    """Count the number of patterns that can be built using the available towel patterns."""
    return sum(is_possible(towels, p) for p in patterns)


@cache
def n_possible(towels: tuple[str, ...], pattern: str) -> int:
    """
    Determine number of ways the display pattern can be built using the available towel patterns.

    It is assumed that the onsen has essentially unlimited towel patterns available to use for
    making each design. Towels cannot be reversed, as this would make the onsen logo face the wrong
    way and that is unacceptable.
    """
    # Shockingly, we can use basically the same recursion as Part 1, but instead sum the number of
    # valid permutations rather than returning early when a pattern is successfully found.
    return not pattern or sum(
        n_possible(towels, pattern[len(t) :]) for t in towels if pattern.startswith(t)
    )


def count_n_possible(towels: tuple[str, ...], patterns: list[str]) -> int:
    """Count the number of permutations that successfully build the desired target patterns."""
    return sum(n_possible(towels, p) for p in patterns)


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    towels, patterns = parse_onsen_station(puzzle_input)

    print(f"Part One: {count_possible(towels, patterns)}")
    print(f"Part Two: {count_n_possible(towels, patterns)}")
