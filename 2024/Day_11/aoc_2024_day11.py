import math
from collections import abc, defaultdict
from pathlib import Path


def parse_stones(raw_stones: str) -> list[int]:
    """
    Parse the provided stone layout into its stone components.

    Stones are assumed to be specified by a single line of space-delimited integers, denoting the
    value engraved on the stone, e.g. `"0 1 10 99 999"`.
    """
    return [int(n) for n in raw_stones.split()]


def blink(stones: abc.Iterable[int]) -> list[int]:
    """
    Model the behavior of the values of the provided stones when the observer blinks.

    Every time the observer blinks, the stones each simultaneously change according to the first
    applicable rule in the following list:
        * If the stone is engraved with the number `0`, it is replaced by a stone engraved with the
        number `1`.
        * If the stone is engraved with a number that has an even number of digits, it is replaced
        by two stones. The left half of the digits are engraved on the new left stone, and the right
        half of the digits are engraved on the new right stone. Note that the new numbers don't keep
        extra leading zeroes: `1000` would become stones `10` and `0`.
        * If none of the other rules apply, the stone is replaced by a new stone; the old stone's
        number multiplied by `2024` is engraved on the new stone.

    No matter how the stones change, their order is preserved, and they stay on their perfectly
    straight line.

    WARNING: This is a brute-force approach that is unlikely to scale well as the number of stones
    becomes large.
    """
    new_stones = []
    for s in stones:
        if s == 0:
            new_stones.append(1)
        elif (math.floor(math.log10(s) + 1) % 2) == 0:  # Even number of digits
            ss = str(s)
            mp = len(ss) // 2
            new_stones.extend(int(n) for n in (ss[:mp], ss[mp:]))
        else:
            new_stones.append(s * 2024)

    return new_stones


def blink_n_counts(start_stones: abc.Iterable[int], n_blinks: int) -> int:
    """
    Determine the number of stones present after the specified number of blinks have been blunked.

    See the documentation for `blink` for an enumeration of the stone value change rules while the
    observer is blinking.

    NOTE: This function does not attempt to retain any knowledge of stone ordering as the blinks are
    blinking.
    """
    # For the purposes of today's puzzle, knowing the stone ordering isn't actually important so we
    # don't actually need to keep track of it as we're blinking. Keeping track of the stone counts
    # should help keep the total runtime manageable for a large number of blinks
    stone_counts: dict[int, int] = defaultdict(int)
    for s in start_stones:
        stone_counts[s] += 1

    for _ in range(n_blinks):
        new_counts: dict[int, int] = defaultdict(int)
        for s, c in stone_counts.items():
            if s == 0:
                new_counts[1] += c
            elif (math.floor(math.log10(s) + 1) % 2) == 0:  # Even number of digits
                ss = str(s)
                mp = len(ss) // 2

                left = int(ss[:mp])
                right = int(ss[mp:])

                new_counts[left] += c
                new_counts[right] += c
            else:
                new_counts[s * 2024] += c

        stone_counts = new_counts

    return sum(stone_counts.values())


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    brute_stones = parse_stones(puzzle_input)
    for _ in range(25):
        brute_stones = blink(brute_stones)

    print(f"Part One: {len(brute_stones)}")
    print(f"Part Two: {blink_n_counts(parse_stones(puzzle_input), 75)}")
