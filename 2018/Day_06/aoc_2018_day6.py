from pathlib import Path


def _parse_coordinates(puzzle_input: list[str]) -> list[tuple[int, int]]:
    """Parse the puzzle input into a list of (x,y) coordinate tuples."""
    coords = []
    for line in puzzle_input:
        x, y = line.split(",")
        coords.append((int(x), int(y)))

    return coords


if __name__ == "__main__":
    puzzle_input_file = Path("puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().splitlines()

    # print(f"Part One: {react_polymer(puzzle_input)}")
    # print(f"Part Two: {improve_polymer(puzzle_input)}")
