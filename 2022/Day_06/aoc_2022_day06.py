from pathlib import Path

import more_itertools as miter


def locate_start_marker(data_buffer: str, chunk_width: int = 4) -> int:
    """
    Identify the 1st position where the `chunk_width` most recently received characters all differ.

    Start marker location is indexed as the number of characters from the beginning of the buffer to
    the end of the first start marker.
    """
    for offset, chunk in enumerate(miter.sliding_window(data_buffer, chunk_width)):
        if len(set(chunk)) == len(chunk):
            return chunk_width + offset

    raise ValueError("Could not locate a start marker for the given data buffer.")


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    print(f"Part One: {locate_start_marker(puzzle_input, chunk_width=4)}")
    print(f"Part Two: {locate_start_marker(puzzle_input, chunk_width=14)}")
