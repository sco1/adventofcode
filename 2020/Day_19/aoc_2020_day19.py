import re
from pathlib import Path


RULESET_T = dict[str, str]


def parse_rules(raw_rules: str, mod_ruleset: bool) -> RULESET_T:
    """
    Parse the provided validation ruleset into a dictionary.

    If `mod_ruleset` is `True`, the ruleset is modified per the description provided in Part Two.
    """
    ruleset = {}
    for line in raw_rules.splitlines():
        rule, _, rule_str = line.partition(":")

        # Keep key as string so we don't have to do a conversion dance in the resolver
        # Strip out quotes for the match characters
        ruleset[rule] = rule_str.strip().replace('"', "")

    # Swap in rule modifications as described by Part Two
    if mod_ruleset:
        ruleset["8"] = "42 | 42 8"
        ruleset["11"] = "42 31 | 42 11 31"

    return ruleset


def parse_message(raw_message: str, mod_ruleset: bool) -> tuple[RULESET_T, list[str]]:
    """Split the recieved transmission into the validation ruleset & messages to validate."""
    raw_rules, messages = raw_message.split("\n\n")

    return parse_rules(raw_rules, mod_ruleset), messages.splitlines()


def _resolver(ruleset: RULESET_T, char: str = "0") -> str:  # Start with rule 0
    """
    Recurse through the rules in the ruleset & resolve references down to character matches.

    NOTE: Rules are assumed to contain no loops
    NOTE: Charater matching rules are assumed to contain a single character
    """
    # Pass the regex OR pipe straight through
    if char == "|":
        return char

    # Pass letter matches straight through, these are assumed to be single letters
    rule = ruleset[char]
    if len(rule) == 1:
        return rule

    # Wrap each subrule in parentheses to preserve its matching as its substituted in
    return f"({''.join(_resolver(ruleset, nchar) for nchar in rule.split())})"


def resolve_ruleset(ruleset: RULESET_T) -> re.Pattern:
    """Resolve the provided ruleset into a compiled regex for checking message validity."""
    return re.compile(_resolver(ruleset))


def check_unmodded(ruleset: RULESET_T, messages: list[str]) -> int:
    """Check a ruleset, which does not contain loops, for valid messages."""
    validator = resolve_ruleset(ruleset)

    n_valid = 0
    for message in messages:
        if validator.fullmatch(message):
            n_valid += 1

    return n_valid


def check_modded(ruleset: RULESET_T, messages: list[str]) -> int:
    """
    Check a modified ruleset, which can contain loops, for valid messages.

    NOTE: This approach is tailored specifically to the puzzle & sample inputs, which contain
    simplifying assumptions:
        * Rule 0 will be "8 11"
        * Rules 8 and 11 are the only rules with loops
        * Rules 42 and 31 are the only rules referenced by Rules 8 and 11
    """
    # The problem statement provides a couple hints for the modifications made to the two rules, by
    # pointing us towards the fact that we're essentially parsing a regex grammar.
    #
    # The change to rule 8 ("42" -> "42 | 42 8") is equivalent to the "+" regex quantifier, giving
    # us "<42>+", and the change to rule 11 ("42 31" -> "42 31 | 42 11 31") is also along the same
    # lines, giving us <42>+<31>.
    #
    # We also get the helpful hint that we only really need to handle the rules that are related to
    # our changes.
    #
    # Since rule 11 is composed of rule 8, we can check a message to see how many times it matches
    # rule 42, and then how many times it matches rule 31. With rule 0 always being "8 11", the
    # subpattern to match becomes "^<42>+<42>+<31>$", so we need to match 31 at least once and 42 at
    # least twice, with 31 anchoring the line.
    rule_31 = re.compile(_resolver(ruleset, "31"))
    rule_42 = re.compile(_resolver(ruleset, "42"))

    n_valid = 0
    for message in messages:
        cursor = 0

        n_match_42 = 0
        while match := rule_42.match(message, pos=cursor):
            n_match_42 += 1
            cursor = match.end()

        n_match_31 = 0
        while match := rule_31.match(message, pos=cursor):
            n_match_31 += 1
            cursor = match.end()

        # Check against "^<42>+<42>+<31>$"
        # 31 must match at least once
        # 42 must match at least one more time than 31
        # 31 must end the message, so our cursor position should be there
        if (0 < n_match_31 < n_match_42) and (cursor == len(message)):
            n_valid += 1

    return n_valid


def check_messages(puzzle_input: str, mod_ruleset: bool = False) -> int:
    """
    Count the number of valid messages recieved based on the provided validator.

    If `mod_ruleset` is `True`, the ruleset is modified per the description provided in Part Two.
    """
    ruleset, messages = parse_message(puzzle_input, mod_ruleset)

    if mod_ruleset:
        return check_modded(ruleset, messages)
    else:
        return check_unmodded(ruleset, messages)


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text()

    print(f"Part One: {check_messages(puzzle_input)} valid messages")
    print(f"Part Two: {check_messages(puzzle_input, mod_ruleset=True)} valid messages")
