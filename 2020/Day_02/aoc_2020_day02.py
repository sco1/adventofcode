import re
import typing as t
from pathlib import Path


class PasswordSpec(t.NamedTuple):
    """Helper class for representing a given corporate password policy specification."""

    key_l: int  # Minimum occurrences (Spec 0) or index (Spec 1)
    key_r: int  # Maximum occurrences (Spec 0) or index (Spec 1)
    key_letter: str

    def is_valid_password(self, password: str, spec: int = 0) -> bool:
        """
        Check if the provided password matches the specified corporate policy specification.

        * Spec 0 checks the keys against occurrences of the key letter
        * Spec 1 checks the keys as indices for exactly one occurrence of the key letter
        """
        if spec == 0:
            return self.key_l <= password.count(self.key_letter) <= self.key_r
        elif spec == 1:
            # Split these into separate lines since black murders the one-line
            left = password[self.key_l - 1] == self.key_letter
            right = password[self.key_r - 1] == self.key_letter

            return left != right  # Need an xor


def parse_passwords(puzzle_input: list[str]) -> list[tuple[PasswordSpec, str]]:
    """
    Parse the provided puzzle input into its password specifications & test passwords.

    Puzzle input is assumed to be of the following form:
        <min occurrences>-<max occurrences> <letter>: <test password>

        e.g. "1-3 a: abcde"
    """
    input_spec = r"(\d+)-(\d+) ([A-Za-z]): ([A-Za-z]+)"

    parsed_out = []
    for line in puzzle_input:
        matched_groups = re.findall(input_spec, line)[0]

        parsed_out.append(
            (
                PasswordSpec(int(matched_groups[0]), int(matched_groups[1]), matched_groups[2]),
                matched_groups[3],
            )
        )

    return parsed_out


def n_valid_passwords(to_check: list[tuple[PasswordSpec, str]], spec_type: int = 0) -> int:
    """
    Count the number of valid passwords according to the two policy spec interpretations.

    * Spec 0 checks the keys against occurrences of the key letter
    * Spec 1 checks the index (1-indexed) of the keys in the password for at least one match of
    the key letter
    """
    n_valid = 0
    for spec, password in to_check:
        if spec.is_valid_password(password, spec_type):
            n_valid += 1

    return n_valid


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().splitlines()

    parsed_input = parse_passwords(puzzle_input)
    print(f"Part One: {n_valid_passwords(parsed_input)} valid passwords")
    print(f"Part Two: {n_valid_passwords(parsed_input, spec_type=1)} valid passwords")
