from collections import Counter, abc
from pathlib import Path


def split_id_locations(raw_location_ids: abc.Iterable[str]) -> tuple[list[int], list[int]]:
    """
    Parse ID groups from the raw list provided by The Historians.

    The raw list is assumed to be provided as one or more rows of space-delimited pairs of integers,
    e.g.:

    ```
    3   4
    4   3
    2   5
    ```

    The provided IDs are split into their left and right columns & sorted in ascending order.
    """
    left_group = []
    right_group = []
    for line in raw_location_ids:
        left, right = line.split()
        left_group.append(int(left))
        right_group.append(int(right))

    return sorted(left_group), sorted(right_group)


def calculate_total_distance(left_group: abc.Iterable[int], right_group: abc.Iterable[int]) -> int:
    """
    Calculate the total distance between the two provided groups of IDs.

    The total distance score is calculated as the sum of the pairwise distances between each ID in
    the provided ID groups. Pairs are grouped by the ID's relative order in their respective group,
    e.g. the smallest left is paired with the smallest right, second-smallest left is paired with
    the second-smallest right, etc.

    NOTE: ID groups are assumed to already be sorted in ascending order.
    """
    return sum(abs(l_id - r_id) for l_id, r_id in zip(left_group, right_group))


def calculate_similarity_score(
    left_group: abc.Iterable[int], right_group: abc.Iterable[int]
) -> int:
    """
    Calculate the similarity score between the two provided groups of IDs.

    The similarity score is calculated by multiplying each ID in the left group by their number of
    occurrences in the right group.
    """
    right_counts = Counter(right_group)
    similarity_score = sum(n * right_counts[n] for n in left_group)

    return similarity_score


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip().splitlines()
    left_group, right_group = split_id_locations(puzzle_input)

    print(f"Part One: {calculate_total_distance(left_group, right_group)}")
    print(f"Part Two: {calculate_similarity_score(left_group, right_group)}")
