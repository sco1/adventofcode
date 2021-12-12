import statistics
from collections import deque
from pathlib import Path

OPENING = {"(": ")", "[": "]", "{": "}", "<": ">"}
CLOSING = {v: k for k, v in OPENING.items()}

SYNTAX_SCORE = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}
AUTOCOMPLETE_SCORE = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


def parse_subsystem_code(navigation_subsystem: list[str]) -> tuple[int, list[str]]:
    """
    Calculate the syntax error score for the provided navigation subsystem code.

    The total score is calculated by taking the first illegal character on each line and allocating
    a per-line score based on the `SYNTAX_SCORE` scoring table. Line scores are then summed to give
    the final subsystem syntax error score.

    Valid code lines are assumed to be incomplete. For each incomplete line, a string is generated
    that completes the line. These lines are returned along with the final syntax error score.
    """
    # Since we don't need to do any evaluation of the contents inside of each scope, we can get away
    # with just keeping track of a stack of opening brackets and ensuring they're being closed
    total_score = 0
    autocomplete_strings = []
    for line in navigation_subsystem:
        bracket_stack = deque()
        for char in line:
            if char in OPENING:
                bracket_stack.append(char)
            elif char in CLOSING:
                # Check that this is closing the last thing in the stack
                # If not, then we can add its score & move to the next line
                if bracket_stack[-1] != CLOSING[char]:
                    total_score += SYNTAX_SCORE[char]
                    break
                else:
                    bracket_stack.pop()
        else:
            # If we get here, the line has correct syntax but is incomplete
            autocomplete_strings.append("".join(OPENING[char] for char in reversed(bracket_stack)))

    return total_score, autocomplete_strings


def score_autocomplete(autocomplete_strings: list[str]) -> int:
    """
    Calculate the autocomplete score for the provided autocomplete strings.

    The autocomplete score is determined by considering the string required to complete each line
    character-by-character. For each character, multiply the total score by 5 and then increase the
    total score by the point value given by `AUTOCOMPLTE_SCORE` for the corresponding character.

    The winning score is the median score; it is assumed that the number of incomplete lines in the
    subsystem will always be odd, so no interpolation is needed.
    """
    scores = []
    for line in autocomplete_strings:
        score = 0
        for char in line:
            score *= 5
            score += AUTOCOMPLETE_SCORE[char]

        scores.append(score)

    return statistics.median(scores)


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().splitlines()

    # Non-corrupted lines are all assumed to be incomplete
    syntax_score, autocomplete_strings = parse_subsystem_code(puzzle_input)

    print(f"Part One: {syntax_score}")
    print(f"Part Two: {score_autocomplete(autocomplete_strings)}")
