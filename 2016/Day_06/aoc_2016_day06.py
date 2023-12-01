from collections import Counter
from pathlib import Path


def correct_message(signal: str, most_common: bool = True) -> str:
    """
    Parse the provided signal and decypher the repetition coded message.

    If the `most_common` flag is `True`, the message is assumed to be composed of the most common
    letter of each column, otherwise the least common letter is used. Each column is assumed to
    contain the same number of characters.
    """
    lines = signal.splitlines()
    n_cols = len(lines[0])

    columns: list[list[str]] = [[] for _ in range(n_cols)]
    for line in lines:
        for col, c in zip(columns, line):
            col.append(c)

    counts = [Counter(col) for col in columns]

    if most_common:
        return "".join(c.most_common(1)[0][0] for c in counts)
    else:
        return "".join(c.most_common()[-1][0] for c in counts)


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    print(f"Part One: {correct_message(puzzle_input)}")
    print(f"Part Two: {correct_message(puzzle_input, most_common=False)}")
