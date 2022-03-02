from functools import cache
from pathlib import Path
from string import ascii_lowercase, ascii_uppercase


def _build_pairs() -> list[str]:
    """Return a list of pairs of caseswapped ASCII characters."""
    out = [f"{letter}{letter.upper()}" for letter in ascii_lowercase]
    out += [pair.swapcase() for pair in out]

    return out


REACTING_PAIRS = _build_pairs()


@cache
def react_polymer(polymer: str) -> int:
    """
    React the polymer until it is fully reacted and return its size.

    The polymer's units' types are represented by letters; units' polarity is represented by
    capitalization. During the reaction, if two adjacent units have the same type and opposite
    polarity then they are destroyed.

    NOTE: Reactions are assumed to occur atomically, so only one reaction can occur at a time.
    """
    pre = len(polymer)
    while True:
        for pair in REACTING_PAIRS:
            polymer = polymer.replace(pair, "")

        # If the polymer length hasn't changed, then the reaction is complete
        reacted_length = len(polymer)
        if reacted_length == pre:
            break
        else:
            pre = reacted_length

    return reacted_length


def improve_polymer(polymer: str) -> int:
    """Locate the unit type that, when removed, minimizes the resulting reacted polymer."""
    # Swap out each letter & rerun part 1 to see which is the best to remove
    return min(
        (
            react_polymer(polymer.replace(lletter, "").replace(uletter, ""))
            for lletter, uletter in zip(ascii_lowercase, ascii_uppercase)
        )
    )


if __name__ == "__main__":
    puzzle_input_file = Path("puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    print(f"Part One: {react_polymer(puzzle_input)}")
    print(f"Part Two: {improve_polymer(puzzle_input)}")
