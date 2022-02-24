import collections
from pathlib import Path


def _validate_password(password: str, check_anagram: bool = False) -> bool:
    """
    Validate the provided password.

    A password is considered valid if it contains no duplicate words. If `check_anagram` is `True`,
    the password also cannot contain any words that can be rearranged to form any other word.
    """
    if check_anagram:
        # If 2 words are anagrams, their sorted characters will be the same
        # e.g. "acbde" and "ecdab" both resolve to "abcde"
        sorted_chars = ["".join(sorted(word)) for word in password.split()]
        word_count = collections.Counter(sorted_chars)
    else:
        word_count = collections.Counter(password.split())

    if max(word_count.values()) == 1:
        return True
    else:
        return False


def validate_password_list(passwords: list[str], check_anagram: bool = False) -> int:
    """
    Count the number of valid passwords in the provided password list.

    A password is considered valid if it contains no duplicate words. If `check_anagram` is `True`,
    the password also cannot contain any words that can be rearranged to form any other word.
    """
    return sum(_validate_password(password, check_anagram) for password in passwords)


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().splitlines()

    print(f"Part One: {validate_password_list(puzzle_input)}")
    print(f"Part Two: {validate_password_list(puzzle_input, check_anagram=True)}")
