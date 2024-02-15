from pathlib import Path

# Initialize some helper collections of letters for easier checking
VALID_LETTERS = "abcdefghjkmnnpqrstuvwxyz"
INVALID_LETTERS = "iol"  # Shouldn't be necessary but defined for the generic case
DOUBLED_LETTERS = [letter * 2 for letter in VALID_LETTERS]
LETTER_RUNS = [VALID_LETTERS[i : i + 3] for i in range(len(VALID_LETTERS) - 2)]
NEXT_LETTER = dict(zip(VALID_LETTERS, VALID_LETTERS[1:] + "a"))  # Add 'a' to wrap 'z'
NEXT_LETTER.update({"i": "j", "o": "p", "l": "m"})  # Add for the generic case


def has_letter_run(in_str: str) -> bool:
    """Check that the input string contains at least 1 run of 3 consecutive valid letters."""
    return any(run in in_str for run in LETTER_RUNS)


def has_invalid_letters(in_str: str) -> bool:
    """Check if the input string contains any invalid letters."""
    return any(letter in in_str for letter in INVALID_LETTERS)


def has_two_doubled_letters(in_str: str) -> bool:
    """Check if input string contains at least 2 different non-overlapping pairs of letters."""
    n_pairs = 0
    for pair in DOUBLED_LETTERS:
        if pair in in_str:
            n_pairs += 1

        if n_pairs >= 2:
            return True
    else:
        return False


def check_valid_password(password: str) -> bool:
    """Helper wrapper to check the input password against the password rules."""
    return all(
        (
            has_letter_run(password),
            not has_invalid_letters(password),
            has_two_doubled_letters(password),
        )
    )


def increment_password(password: str) -> str:
    """
    Increment the input password.

    Incrementing logic is as follows:
        * Increment the last character of the password
        * If the increment wraps around, repeat above with the next letter to the left until one
          does not wrap around
    """
    tmp_password = list(password)  # Temporarily cast to list so we can edit in place
    for i in range(-1, -len(password) - 1, -1):  # Iterate backwards & provide an index
        tmp_password[i] = NEXT_LETTER[tmp_password[i]]

        if tmp_password[i] != "a":
            # We haven't wrapped around
            break

    return "".join(tmp_password)


def generate_new_password(password: str) -> str:
    """
    Generate the next valid password for Santa based on the rules provided in the Problem Statement.

    Due to the function's while loopiness, the number of iterations is limited by `max_iter`
    """
    iter = 0
    while True:
        # Increment once so we don't return if the input is valid
        password = increment_password(password)
        if not check_valid_password(password):
            password = increment_password(password)
            iter += 1
        else:
            return password, iter


puzzle_input_file = Path("./puzzle_input.txt")
with puzzle_input_file.open(mode="r") as f:
    puzzle_input = f.read()

first_password, n_iter = generate_new_password(puzzle_input)
print(f"{first_password} ({n_iter} iterations)")

second_password, n_iter = generate_new_password(first_password)
print(f"{second_password} ({n_iter} iterations)")
