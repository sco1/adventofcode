import re
from pathlib import Path

MAP_RE = re.compile(r"Valve (\w+).*rate=(\d+);.*valves? (.*)")


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text()

    print(f"Part One: {...}")
    print(f"Part Two: {...}")
