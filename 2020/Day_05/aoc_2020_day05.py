from pathlib import Path


def decode_boarding_pass(specifier: str) -> tuple[int, int, int]:
    """
    Decode the boarding pass specifier into its row & column numbers, along with seat ID.

    The seat is encoded into a 10 character pattern:
        * The first 7 letters encode the row into "F" or "B", for rows [0, 127]
        * The final 3 letters encode the column into "L" or "R", for columns [0, 7]

    Seat ID is defined as 8*row + column.
    """
    # From the problem statement, we can figure out that this is a binary encoding in disguise!
    specifier = specifier.replace("F", "0").replace("B", "1")
    specifier = specifier.replace("L", "0").replace("R", "1")

    # We can use the full binary encoding & some binary operations to get out the desired values
    decoded_id = int(specifier, 2)

    # With row being the first 7 digits, we can right-shift to drop off the trailing column encoding
    row = decoded_id >> 3

    # With column being the final 3 digits, we can use a bit mask (binary AND) to get their state
    column = decoded_id & 7  # 7 -> 0000000111

    return row, column, (8 * row + column)


def find_my_seat(decoded_seat_ids: set[int]) -> int:
    """
    Given an index of all other occupied seats on the aircraft, find the seat I should be in.

    The flight is assumed to be completely full, so the seats around mine will be occupied.

    Seats at the very front and back of the plane don't exist on the aircraft, so they will not be
    in the list of boarding passes. Per the problem statement, we're not in the front or back.
    """
    # Use a sliding window to find the unoccupied seat
    for test_id in range(min(decoded_seat_ids), max(decoded_seat_ids) + 1):
        if test_id not in decoded_seat_ids:
            # Empty seat, check around it
            if (test_id - 1) in decoded_seat_ids and (test_id + 1) in decoded_seat_ids:
                # The seats around it are occupied, so this is our seat!
                return test_id


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().splitlines()

    all_seat_ids = {decode_boarding_pass(specifier)[2] for specifier in puzzle_input}
    print(f"Part One: The maximum seat ID is {max(all_seat_ids)}")
    print(f"Part Two: My seat ID is {find_my_seat(all_seat_ids)}")
