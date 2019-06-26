from collections import Counter, deque
from itertools import groupby
from pathlib import Path
from typing import List, Tuple


def is_nice_a(word: str) -> bool:
    """
    Check if a word is naughty or nice.

    A nice word is determined by the following criteria:
        * Contains at least 3 vowels (aeiou)
        * Contains at least one letter that appears twice in a row
        * Does not contain the strings 'ab', 'cd', 'pq', or 'xy'
    """
    word = word.lower()  # Normalize to lowercase

    # Check for vowels
    vowels = ["a", "e", "i", "o", "u"]
    vowel_count = [word.count(vowel) for vowel in vowels]
    if sum(vowel_count) < 3:
        return False

    # Check for consecutive duplicate characters
    consecutive_duplicates = [True for _, group in groupby(word) if len(list(group)) > 1]
    if not consecutive_duplicates:
        return False

    # Check for naughty substrings
    naughty_substrings = ("ab", "cd", "pq", "xy")
    if any(substring in word for substring in naughty_substrings):
        return False

    # If we get this far we have a nice word!
    return True


def is_nice_b(word: str) -> bool:
    """
    Check if a word is naughty or nice.

    A nice word is determined by the following criteria:
        * Contains a pair of any two letters that appear at least twice without overlapping
        * Contains at least one letter which repeats with exactly one letter between
    """
    word = word.lower()  # Normalize to lowercase

    # Check for duplicate letter pairs by splitting into 2-character strings & checking counts
    chunk_counts = Counter(rolling_window(word, 2))
    if all(count == 1 for count in chunk_counts.values()):
        return False

    # Check each 3-character chunk to see if the first letter is the same as the last
    if not any(chunk[0] == chunk[-1] for chunk in rolling_window(word, 3)):
        return False

    # If we get this far we have a nice word!
    return True


def rolling_window(word: str, window_size: int) -> str:
    """Rolling window of characters from the input string."""
    window = deque(maxlen=2)
    for idx, char in enumerate(word):
        if idx < (window_size - 1):
            window.append(char)
        else:
            window.append(char)
            yield "".join(list(window))


def check_word_list(word_list: List[str]) -> Tuple[int]:
    """Count the number of nice words in the input word list based on the two rulesets"""
    rule_a_count = [is_nice_a(word) for word in word_list].count(True)
    rule_b_count = [is_nice_b(word) for word in word_list].count(True)
    return rule_a_count, rule_b_count


puzzle_input_file = Path("./puzzle_input.txt")
with puzzle_input_file.open(mode="r") as f:
    puzzle_input = f.readlines()

print(check_word_list(puzzle_input))
