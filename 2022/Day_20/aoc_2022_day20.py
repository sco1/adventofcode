import typing as t
from pathlib import Path

DECRYPTION_KEY = 811_589_153


def parse_file(raw_file: str) -> list[int]:  # noqa: D103
    return [int(line) for line in raw_file.splitlines()]


def decrypt(
    encrypted: t.Sequence[int],
    query_idx: t.Iterable[int] = (1000, 2000, 3000),
    decryption_key: int = 1,
    n_rounds: int = 1,
) -> int:
    """
    Decrypt the provided encrypted file by mixing & extract the grove coordinates.

    To decrypt the file file, each number is moved forward or backward in the file a number of
    positions equal to its value. The numbers should be moved in the order they originally appear in
    the encrypted file. Numbers moving around during the mixing process do not change the order in
    which the numbers are moved. The list is circular, so moving a number off one end of the list
    wraps back around to the other end as if the ends were connected.

    Grove coordinates are found by summing the values found at the specified query indices.

    To support additional decryption routines, `decryption_key` and `n_rounds` may be specified to
    alter the procedure:
        * If `decryption_key` is a value other than `1`, all encrypted values are multiplied by the
        given key
        * `n_rounds` alters the number of mixing rounds conducted prior to calculating the grove
        coordinates
    """
    if decryption_key != 1:
        encrypted = [v * decryption_key for v in encrypted]

    n_vals = len(encrypted)
    mix_idx = list(range(n_vals))
    for _ in range(n_rounds):
        # Perform the mixing by calculating how our indices are changing during each swap, then use
        # the indices to map back to the original values to obtain the newly ordered list
        for idx, val in enumerate(encrypted):
            loc = mix_idx.index(idx)
            mix_idx.pop(loc)

            # Use n-1 because we're shifting the other values without considering where the shifted
            # value currently is
            shifted = (loc + val) % (n_vals - 1)

            if shifted == 0:
                # Moving to the 0th spot puts us before the existing 0th number; since the list is
                # circular this ends up wrapping us back to the end
                # Equivalent to appending, if we say -1 then it puts us before the last value
                shifted = n_vals

            mix_idx.insert(shifted, idx)

    decrypted = [encrypted[i] for i in mix_idx]
    zero_idx = decrypted.index(0)
    return sum(decrypted[(v + zero_idx) % n_vals] for v in query_idx)


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text()

    encrypted = parse_file(puzzle_input)
    print(f"Part One: {decrypt(encrypted)}")
    print(f"Part Two: {decrypt(encrypted, decryption_key=DECRYPTION_KEY, n_rounds=10)}")
