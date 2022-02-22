import json
from pathlib import Path
from typing import Union


def accounting_sum(entry: Union[list, dict, str, int], ignore_red: bool = False) -> int:
    """
    Recursively sum all integers present in Santa's terrible accounting system.

    Entries in Santa's accounting system consists of lists, dicts, strings, and integers

    Per the problem statement, strings are assumed to have no digits

    `ignore_red` can be set to ignore any dictionaries keys with 'red' as a value
    """
    if isinstance(entry, list):
        return sum([accounting_sum(item, ignore_red) for item in entry])

    if isinstance(entry, dict):
        if ignore_red and "red" in entry.values():
            return 0
        else:
            return sum([accounting_sum(item, ignore_red) for item in entry.values()])

    if isinstance(entry, str):
        return 0

    if isinstance(entry, int):
        return entry


puzzle_input_file = Path("./puzzle_input.json")
with puzzle_input_file.open(mode="r") as f:
    puzzle_input = json.load(f)

print(accounting_sum(puzzle_input))
print(accounting_sum(puzzle_input, ignore_red=True))
