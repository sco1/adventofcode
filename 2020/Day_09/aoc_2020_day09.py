import typing as t
from collections import abc, deque
from itertools import combinations, islice
from pathlib import Path


def combo_sums(int_pool: t.Deque[int], pick_n: int = 2) -> abc.Iterator[int]:
    """Yield the sum of `pick_n` length subsequences of elements from the provided integer pool."""
    for combo in combinations(int_pool, pick_n):
        yield sum(combo)


def rolling_window(int_stream: list[int], window_width: int) -> abc.Iterator[tuple[int]]:
    """Return rolling windows, of width `window_width`, of items from the input iterable."""
    # Use islice to populate the deque from the input iterator rather than using a for loop
    rolling_window = deque(islice(int_stream, window_width), maxlen=window_width)
    yield tuple(rolling_window)  # Yield the first window

    for thing in int_stream:
        rolling_window.append(thing)
        yield tuple(rolling_window)


def process_stream(int_stream: list[int], preamble_len: int = 25) -> int:
    """
    Scan the provided integer stream for the first invalid number.

    A number is considered invalid if it's not equal to the sum of any of the two `preamble_len`
    immediately previous numbers. The first `preamble_len` numbers are ignored.
    """
    window = deque(int_stream[:preamble_len], maxlen=preamble_len)
    stream_queue = deque(int_stream[preamble_len:])

    while stream_queue:
        check_val = stream_queue.popleft()
        if not any(check_val == checksum for checksum in combo_sums(window)):
            return check_val
        else:
            window.append(check_val)


def find_weakness(int_stream: list[int], preamble_len: int = 25) -> int:
    """
    Scan the provided integer stream for the encryption weakness.

    The encryption weakness is identified as the sum of the smallest & largest numbers in a
    contiguous set of numbers in the provided input stream that equals the weakness identified by
    `process_stream`.

    The minimum set width is 2.
    """
    target_checksum = process_stream(int_stream, preamble_len)
    maxwidth = len(int_stream) - 2  # Minimum of at least 2 numbers

    # Calculate the sum of expanding width rolling windows until a match is found
    for width in range(2, maxwidth + 1):
        for window in rolling_window(int_stream, width):
            if sum(window) == target_checksum:
                return min(window) + max(window)


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text()

    int_stream = [int(line) for line in puzzle_input.splitlines()]
    print(f"Part One: {process_stream(int_stream)} first misses check")
    print(f"Part Two: The encryption weakness is {find_weakness(int_stream)}")
