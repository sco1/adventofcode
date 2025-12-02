import math
import re
import typing as t
from collections import abc
from pathlib import Path


class ProductIDRange(t.NamedTuple):  # noqa: D101
    start: int
    end: int

    @classmethod
    def from_raw(cls, raw_id: str) -> t.Self:
        """
        Parse a product ID range from its raw description.

        Product ID ranges are assumed to be of the form: `<start>-<end>`, where IDs are specified
        as positive integers.
        """
        start, end = raw_id.split("-")
        return cls(int(start), int(end))


def is_valid_id(product_id: int) -> bool:
    """
    Determine if the provided product ID is valid.

    An ID is considered valid if it is not made up of some sequence of digits repeated twice.

    For example:
        * `11` - Invalid
        * `12` - Valid
        * `998` - Valid
        * `1010` - Invalid
    """
    # Since invalid IDs have a repeated pattern, they must have an even number of digits so we can
    # short-circuit here
    n_digits = math.floor(math.log10(product_id)) + 1  # floor+1 vs ceil to accomodate 0
    if n_digits % 2 != 0:
        return True

    id_str = str(product_id)
    left, right = id_str[: len(id_str) // 2], id_str[len(id_str) // 2 :]
    return left != right


# Anchored at the start of the string, find a group of one or more digits that repeats at least once
REPEAT_DIGITS_RE = re.compile(r"^(\d+)\1+$")


def is_valid_id_expanded(product_id: int) -> bool:
    """
    Determine if the provided product ID is valid using expanded criteria.

    An ID is considered valid if it is not made up of some sequence of digits repeated at least
    twice.

    For example:
        * `11` - Invalid
        * `12` - Valid
        * `998` - Valid
        * `999` - Invalid
        * `1010` - Invalid
        * `222222` - Invalid
    """
    # I'm sure there's a clever iterative approach, but let's have fun with clever regex :)
    id_str = str(product_id)
    if REPEAT_DIGITS_RE.match(id_str):
        return False
    else:
        return True


def find_invalid_ids(id_range: ProductIDRange, expanded: bool = False) -> list[int]:
    """
    Identify invalid product IDs in the specified range.

    If `expanded` is `True`, the expanded ID validity criteria is utilized.

    NOTE: Product ID ranges are assumed to be inclusive.
    """
    if expanded:
        check_func = is_valid_id_expanded
    else:
        check_func = is_valid_id

    invalid_ids = []
    for query_id in range(id_range.start, id_range.end + 1):
        if not check_func(query_id):
            invalid_ids.append(query_id)

    return invalid_ids


def invalid_id_sum(invalid_ids: abc.Iterable[abc.Iterable[int]]) -> int:  # noqa: D103
    return sum(sum(inner) for inner in invalid_ids)


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    ID_RANGES = [ProductIDRange.from_raw(s) for s in puzzle_input.split(",")]

    p1_sum = invalid_id_sum(find_invalid_ids(id_range) for id_range in ID_RANGES)
    print(f"Part One: {p1_sum}")

    p2_sum = invalid_id_sum(find_invalid_ids(id_range, expanded=True) for id_range in ID_RANGES)
    print(f"Part Two: {p2_sum}")
