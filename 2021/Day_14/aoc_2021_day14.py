import re
from collections import Counter
from pathlib import Path

import more_itertools as mi

INSERTION_RE = re.compile(r"(\w+) -> (\w)")


def parse_polymer_formula(raw_instructions: str) -> tuple[str, dict[str, str]]:
    """
    Parse the provided insertion instructions into its template polymer and insertion rules.

    The first line of the provided raw instructions is assumed to be the template polymer. After the
    template polymer, a blank line is expected, followed by one or more pairwise insertion rules of
    the form `<AB> -> <C>`.
    """
    template, insertions = raw_instructions.split("\n\n")

    rules = {}
    for line in insertions.splitlines():
        left, right = INSERTION_RE.findall(line)[0]
        rules[left] = right

    return template, rules


# Leaving the brute force approach in for posterity, but this approach becomes untenable very
# quickly as the number of steps increases
def polymerize(polymer: str, rules: dict[str, str]) -> str:
    """
    Build a new polymer from the provided starter and pairwise insertion rules.

    Element insertion is determined using a sliding window over the element pairs of the base
    polymer. All insertions are assumed to happen simultaneously, and it is assumed that all polymer
    pairs in the base polymer are present in the insertion rules.
    """
    reacted = []
    for l, r in mi.sliding_window(polymer, 2):  # noqa: E741
        pair = f"{l}{r}"
        reacted.append(l)
        reacted.append(rules[pair])

    # Because we're doing a sliding window, the right side will be the left side of the next pair,
    # so we just need to tack on the final one
    reacted.append(r)

    return "".join(reacted)


def polymerize_cycles(template: str, insertion_formula: dict[str, str], n_cycles: int) -> str:
    """Run the provided template polymer through the provided number of insertion cycles."""
    for _ in range(n_cycles):
        template = polymerize(template, insertion_formula)

    return template


def calculate_spread(polymer: str) -> int:
    """
    Calculate the element spread of the provided polymer.

    Element spread is defined as the difference between the most common and least common elements in
    the polymer.
    """
    element_counts = Counter(polymer).most_common()
    return element_counts[0][1] - element_counts[-1][1]


# How about a smarter not harder approach instead
def non_brute_deconstruct(template: str, rules: dict[str, str], n_cycles: int) -> int:
    """Calculate the element spread of the provided polymer after the target insertion cycle(s)."""
    left: str
    right: str

    # Since we don't care about order, we can keep track of the pairs created by each step and
    # use these counts to determine element counts once we run through all of the insertion cycles
    # Start by initializing with the pairs in our polymer template
    pairs_counter = Counter("".join(window) for window in mi.sliding_window(template, 2))
    for _ in range(n_cycles):
        updated_pairs: Counter[str] = Counter()
        for pair, count in pairs_counter.items():
            left, right = pair
            # Each pair will add the corresponding number of pairs composed of the inserted element
            # and the left/right sides
            # This will end up double counting the middle element but we can fix that later
            updated_pairs[f"{left}{rules[pair]}"] += count
            updated_pairs[f"{rules[pair]}{right}"] += count

        # Now that we've updated our pairs we can replace our starting point
        pairs_counter = updated_pairs

    # Now that we have all the pairs, we can deconstruct them and calculate the composing element
    # quantities. As noted above, our inserted elements have all been double counted, except for the
    # first & last elements. So we can just double the first & last and divide the counts by 2.
    element_counts: Counter[str] = Counter()
    for (left, right), count in pairs_counter.items():
        element_counts[left] += count
        element_counts[right] += count
    element_counts[template[0]] += 1
    element_counts[template[-1]] += 1

    counts = element_counts.most_common()
    return (counts[0][1] - counts[-1][1]) // 2


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text()
    template, rules = parse_polymer_formula(puzzle_input)

    print(f"Part One: {non_brute_deconstruct(template, rules, 10)}")
    print(f"Part Two: {non_brute_deconstruct(template, rules, 40)}")
