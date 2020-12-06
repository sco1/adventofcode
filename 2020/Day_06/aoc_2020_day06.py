from pathlib import Path


def count_any_yes(answer_group: str) -> int:
    """
    Check the number of unique "yes" answers in the provided group answers.

    Answers are expected to be provided as a single line string, where each character represents a
    unique yes-or-no answer where someone in the group has responsed "yes"
    """
    return len(set(answer_group))


def count_all_yes(answer_group: list[str]) -> int:
    """
    Check the number of questions where all group members have answered "yes".

    Answers are expected to be provided as a list of strings, where each string represents the "yes"
    answers for an individual group member.
    """
    if len(answer_group) == 1:
        # Short-circuit if there's only one responder in the group
        return len(answer_group[0])

    answer_sets = [set(member) for member in answer_group]
    return len(answer_sets[0].intersection(*answer_sets[1:]))


def batch_check_forms(batched_answers: str, all_yes: bool = False) -> list[int]:
    """
    Parse the provided batched group answers into a list containing the number of "yes" answers.

    The batched input is assumed to contain one or more letter identifiers for questions where
    anyone in the group has answered "yes" to one of 26 yes-or-no questions (a-z).

    Answers from individual members of the group are delimited by newlines, and groups are delimited
    by a blank line.
    """
    n_yesses = []
    # Split on blank lines to get individual groups
    for group in batched_answers.split("\n\n"):
        if all_yes:
            # Need to keep individual answers separate
            n_yesses.append(count_all_yes(group.splitlines()))
        else:
            # Individual answers don't matter so they can be combined
            n_yesses.append(count_any_yes(group.replace("\n", "")))

    return n_yesses


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text()

    print(f"Part One: {sum(batch_check_forms(puzzle_input))} questions answered 'yes'")
    print(
        f"Part Two: {sum(batch_check_forms(puzzle_input, all_yes=True))} questions all answered 'yes'."  # noqa: E501
    )
