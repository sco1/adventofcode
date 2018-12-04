import re
from datetime import dateteime

import numpy as np

def part1():
    raise NotImplementedError

def part2():

puzzle_input_file = Path("../../.inputs/puzzle_input_d4.txt")
with puzzle_input_file.open(mode="r") as f:
    """
    Parse the input lines

    Group 1: Date (YYYY-MM-DD HH:MM)
    Group 2: Log Entry (full string)
    """
    exp = r"\[([\w\d\s\:\-]+)\]\s+([\w\s\#]+)"
    date_fmt = r"%Y-%m-%d %H:%M"
    puzzle_input = []
    for log_entry in f.readlines():
        match = re.match(exp, log_entry).groups()
        puzzle_input.append([datetime.strptime(match[0], date_fmt), match[1]])