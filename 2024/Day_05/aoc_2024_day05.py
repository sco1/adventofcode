import graphlib
import typing as t
from collections import abc, defaultdict
from pathlib import Path


class PageOrderRule(t.NamedTuple):  # noqa: D101
    pre: int
    post: int


def parse_print_spec(raw_spec: str) -> tuple[list[PageOrderRule], list[list[int]]]:
    """
    Parse the provided printing specification for its page ordering rules and pages to produce spec.

    The incoming specification is assumed to be of the form:

    ```
    X|Y

    A,B,C,D
    ```

    Where page ordering rules are provided as newline-delimited `X|Y` pairs, where page `X` must be
    printed before page `Y` if they are both to be printed in a production specification.

    The pages to produce specification follows the page ordering rules; the two sections are assumed
    to be separated by a single blank line. Pages to produce specifications are provided as
    newline-delimited sequences of comma-separated integers describing the page numbers of each
    proposed update, in order.
    """
    raw_ordering_rules, raw_update_spec = raw_spec.split("\n\n")

    ordering_rules = []
    for rule in raw_ordering_rules.splitlines():
        pre, post = rule.split("|")
        ordering_rules.append(PageOrderRule(int(pre), int(post)))

    update_spec = []
    for update in raw_update_spec.splitlines():
        update_spec.append([int(n) for n in update.split(",")])

    return ordering_rules, update_spec


def compile_order_rules(
    ordering_rules: abc.Iterable[PageOrderRule],
    reversed: bool = False,
) -> dict[int, set[int]]:
    """
    Compile the provided page ordering rules into a mapping of pages -> pages that must follow.

    For example, `[(47, 53), (97, 13), (97, 61)]` is mapped to `{47: {53}, 97: {13, 61}}`,
    indicating that page `47` must be printed sometime before page `53`, and page `97` must
    be printed sometime before pages `13` and `61`.

    If `reversed` is `True`, the mapping is flipped such that the values are pages that must precede
    the key. For example, the previous ruleset would instead be mapped to
    `{53: {47}, 13: {97}, 61: {97}}`.
    """
    compiled_ordering = defaultdict(set)
    for rule in ordering_rules:
        if reversed:
            compiled_ordering[rule.post].add(rule.pre)
        else:
            compiled_ordering[rule.pre].add(rule.post)

    return compiled_ordering


def is_valid_spec(compiled_rules: dict[int, set[int]], spec: list[int]) -> bool:
    """Determine if the provided update specification is in the correct order."""
    for i, spec_p in enumerate(spec):
        # Our compiled rules contain a mapping of pages that must be after spec_p, so if we find
        # one later then the spec is invalid
        for j, check_p in enumerate(spec):
            if (i > j) and (check_p in compiled_rules[spec_p]):
                return False

    return True


def calculate_valid_sum(raw_spec: str) -> int:
    """Calculate the sum of the middle pages of any valid update specifications."""
    ordering_rules, update_spec = parse_print_spec(raw_spec)
    compiled_rules = compile_order_rules(ordering_rules)

    valid_sum = 0
    for spec in update_spec:
        if is_valid_spec(compiled_rules, spec):
            valid_sum += spec[len(spec) // 2]

    return valid_sum


def reorder_spec(compiled_rules: dict[int, set[int]], spec: list[int]) -> list[int]:
    """
    Reorder the provided known-bad update specification so it produces a valid spec.

    The provided compiled ruleset is assumed to be the reversed mapping, i.e. values are the pages
    that must precede the key.
    """
    # This calls for a topological sort! I've never tried out graphlib before so let's try that
    # rather than trying to debug my poor attempts to write my own.
    #
    # Filter the compiled rules down to contain just the pages that are contained in our problem
    # spec, otherwise we may start cycling if the input happens to be deviously crafted
    spec_set = set(spec)
    compiled_rules_filtered = {
        post: pre.intersection(spec_set) for post, pre in compiled_rules.items() if post in spec_set
    }
    ts = graphlib.TopologicalSorter(compiled_rules_filtered)

    # Because the ruleset we're using is reversed, we also need to reverse the resulting static
    # order. Since we're only using the midpoint of this new spec later on this doesn't actually
    # matter, but it does break the unit test :)
    reordered = list(ts.static_order())[::-1]

    return reordered


def calculate_reordered_sum(raw_spec: str) -> int:
    """Calculate the sum of the middle pages of repaired specifications."""
    ordering_rules, update_spec = parse_print_spec(raw_spec)
    compiled_rules = compile_order_rules(ordering_rules)
    reversed_compiled_rules = compile_order_rules(ordering_rules, reversed=True)

    repaired_sum = 0
    for spec in update_spec:
        if not is_valid_spec(compiled_rules, spec):
            repaired = reorder_spec(reversed_compiled_rules, spec)
            repaired_sum += repaired[len(repaired) // 2]

    return repaired_sum


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    print(f"Part One: {calculate_valid_sum(puzzle_input)}")
    print(f"Part Two: {calculate_reordered_sum(puzzle_input)}")
