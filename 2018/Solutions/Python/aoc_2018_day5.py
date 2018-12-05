from pathlib import Path


def part1(puzzle_input: str) -> int:
    raise NotImplementedError

def part2(puzzle_input:str):
    raise NotImplementedError


puzzle_input_file = Path("../../Inputs/puzzle_input_d5.txt")
with puzzle_input_file.open(mode="r") as f:
    puzzle_input = f.readlines()[0]

print(part1(puzzle_input))
print(part2(puzzle_input))