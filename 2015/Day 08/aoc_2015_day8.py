import re
from pathlib import Path
from typing import List


def size_in_code(in_str: str) -> int:
    """
    Return the character length of the given string, including escapes and/or hexadecimal code(s).

    e.g. "aaa\\"aaa" has a length of 10, and "\\x27" has a length of 6

    Note: The above examples contain additonal escapes so they render properly after interpretation
    """
    return len(in_str)


def size_in_memory(in_str: str) -> int:
    """
    Return the interpreted string length of the given string.

    The only assumed valid escapes are: 
        * \\\\  (Backslash)
        * \\"   (Single apostrophe)
        * \\x.. (Single ASCII character, hexadecimal)

    e.g. "aaa\\"aaa" has a length of 7, and "\\x27" has a length of 1

    Note: The above examples contain additonal escapes so they render properly after interpretation
    """
    # Strip quotes
    in_str = in_str[1:-1]

    # Substitute escaped strings for a dummy character (_)
    in_str = in_str.replace(r"\\", "_")
    in_str = in_str.replace(r"\"", "_")
    in_str = re.sub(r"\\x.{2}", "_", in_str)

    return len(in_str)


def size_if_escaped(in_str: str) -> int:
    """
    Calculate the length of the fully escaped version of the input string.

    e.g. "aaa\\"aaa" becomes "\\"aaa\\\\\\"aaa\\"", which has a length of 16

    Note: The above example contains additonal escapes so they render properly after interpretation
    """
    in_str = in_str.replace('"', r"\"")
    in_str = in_str.replace(r"\\", "\\\\\\")
    in_str = in_str.replace(r"\x", r"\\x")

    return len(in_str) + 2  # Add 2 for new surrounding quotes


def list_size_delta(santas_list: List[str]) -> int:
    """Calculate the difference between the size of Santa's list in code vs. in memory."""
    code_size = 0
    memory_size = 0
    for entry in santas_list:
        code_size += size_in_code(entry)
        memory_size += size_in_memory(entry)

    return code_size - memory_size


def escaped_size_delta(santas_list: List[str]) -> int:
    """Calculate the difference between the size of Santa's list w/escaped strings vs. in memory."""
    escaped_size = 0
    code_size = 0
    for entry in santas_list:
        escaped_size += size_if_escaped(entry)
        code_size += size_in_code(entry)

    return escaped_size - code_size


puzzle_input_file = Path("./puzzle_input.txt")
with puzzle_input_file.open(mode="r") as f:
    puzzle_input = [line.strip() for line in f]

print(list_size_delta(puzzle_input))
print(escaped_size_delta(puzzle_input))