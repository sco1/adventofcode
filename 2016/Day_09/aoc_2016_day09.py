from collections import deque
from pathlib import Path


def decompress(compressed: str, recurse: bool = False) -> str:
    """
    Decompress the provided file format.

    Files are compressed using markers to indicate that a subsequence should be repeated. For
    example, `(10x2)` indicates that the next 10 characters should be repeated twice, then continue
    reading the file after the repeated data. The marker is not included in the decompressed output.

    Parentheses or other characters may appear within the data referenced by a marker, this should
    be treated as normal data.
    """
    file = deque(compressed)
    decompressed = []
    while file:
        c = file.popleft()
        if c == "(":
            buffer = []
            # Start of marker, consume until closing )
            while (sub_c := file.popleft()) != ")":
                buffer.append(sub_c)

            n_char, repeat = [int(n) for n in "".join(buffer).split("x")]
            repeat_buffer = [file.popleft() for _ in range(n_char)]

            if recurse:
                decompressed.append(decompress("".join(repeat_buffer), recurse=True) * repeat)
            else:
                decompressed.append("".join(repeat_buffer) * repeat)
        else:
            # Otherwise just normal data
            decompressed.append(c)

    return "".join(decompressed)


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    print(f"Part One: {len(decompress(puzzle_input))}")
    print(f"Part Two: {len(decompress(puzzle_input, recurse=True))}")
