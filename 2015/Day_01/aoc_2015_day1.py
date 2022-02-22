from pathlib import Path


def santa_elevator(instructions: str) -> int:
    """
    Help Santa navigate the large apartment building!

    `instructions` is a string of parentheses, where ( goes up one floor and ) goes down one floor

    Returns the destination floor
    """
    current_floor = 0
    for step in instructions:
        if step == "(":
            current_floor += 1
        elif step == ")":
            current_floor -= 1
        else:
            raise ValueError(f"Unknown instruction: '{step}'")

    return current_floor


def basement_finder(instructions: str) -> int:
    """
    Find where Santa enters the basement!

    `instructions` is a string of parentheses, where ( goes up one floor and ) goes down one floor

    Returns the step index where Santa first enters the basement (floor = -1)
    """
    current_floor = 0
    for idx, step in enumerate(instructions):
        if step == "(":
            current_floor += 1
        elif step == ")":
            current_floor -= 1
        else:
            raise ValueError(f"Unknown instruction: '{step}'")

        if current_floor == -1:
            return idx + 1


puzzle_input_file = Path("./puzzle_input.txt")
with puzzle_input_file.open(mode="r") as f:
    puzzle_input = f.read()

print(santa_elevator(puzzle_input))
print(basement_finder(puzzle_input))
