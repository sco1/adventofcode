import typing as t
from pathlib import Path

import numpy as np


def parse_bingo(puzzle_input: list[str]) -> tuple[list[int], np.ndarray]:
    """
    Parse the provided puzzle input into the list of numbers to draw & the bingo boards to play.

    The first line of the input is assumed to be a comma separated list of numbers to draw, followed
    by one or more bingo boards. There is assumed to be at least one blank line following both the
    numbers to draw and each bingo board. All boards are assumed to be the same size.

    The boards are stacked into a single 3D numpy array.
    """
    draws = [int(draw) for draw in puzzle_input[0].split(",")]
    boards = []
    raw_board = []
    for line in puzzle_input[2::]:
        if not line:
            boards.append(raw_board)
            raw_board = []
        else:
            raw_board.append([int(col) for col in line.split()])
    else:
        # Add any dangling board
        if raw_board:
            boards.append(raw_board)

    return draws, np.array(boards)


def _calculate_final_score(
    winning_num: int, winning_board: np.ndarray, boards: np.ndarray, mask: np.ndarray
) -> int:
    # Find the sum of the uncalled numbers on the winning board
    # Since our mask is called numbers, we can negate it to mask the uncalled numbers instead
    board_sum = boards[winning_board][~mask[winning_board]].sum()
    return board_sum * winning_num


def run_bingo(draws: list[int], boards: np.ndarray) -> t.Generator[int, None, None]:
    """
    Run through the specified number draw and yield the final score for any winning round.

    A bingo board is won if a row or a column are filled; diagonal fills are ignored.

    The final score is calculated by multiplying the winning number by the sum of the numbers
    remaining on the winning board. Boards are not reset & are no longer considered after they have
    won.
    """
    n_boards, n_rows, n_cols = boards.shape
    mask = np.full_like(boards, False, dtype=bool)
    winning_boards = set()
    for num in draws:
        mask[boards == num] = True
        row_sums = np.sum(mask, axis=1)
        col_sums = np.sum(mask, axis=2)

        # Iterate by board so we can keep track of (and skip) boards that have already won
        for idx in range(n_boards):
            if idx in winning_boards:
                continue

            # Check each row (axis=1) & column (axis=2) for any that are fully called
            loc = np.argwhere(row_sums[idx] == n_cols)
            if loc.size > 0:
                yield _calculate_final_score(num, idx, boards, mask)
                winning_boards.add(idx)

            loc = np.argwhere(col_sums[idx] == n_rows)
            if loc.size > 0:
                yield _calculate_final_score(num, idx, boards, mask)
                winning_boards.add(idx)


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().splitlines()
    draws, boards = parse_bingo(puzzle_input)

    winning_boards = list(run_bingo(draws, boards))
    print(f"Part One: {winning_boards[0]}")
    print(f"Part One: {winning_boards[-1]}")
