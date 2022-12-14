import ast
import functools
import itertools
import math
import typing as t
from pathlib import Path

PACKET_PAIR: t.TypeAlias = tuple[list, list]


def parse_packets(packet_stream: str, insert_divider: bool = False) -> t.Iterator[PACKET_PAIR]:
    """
    Parse the provided packet stream into pairs of packets.

    Packets are assumed to be lists, with pairs of packets delimited by a blank line.

    If `insert_divider` is set, an additional pair of divider packets is emitted.
    """
    for pair in packet_stream.split("\n\n"):
        yield tuple(ast.literal_eval(lst) for lst in pair.splitlines())  # type: ignore[misc]

    if insert_divider:
        yield [2], [6]


def check_order(left: list, right: list) -> int:
    """
    Determine whether the provided pair of packets is in the correct order.

    If the packet pair is not in the correct order, the returned value will be negative.

    Packet pairs are compared element-wise, from left to right:
        * If both values are integers, the lower integer should be on the left
        * If both values are lists, compare the elements of each list; if both lists are not the
        same length, the left list should run out values first
        * If one value is a list and the other an integer, the integer should be converted into a
        list whose only value is the iteger, and the comparison run with this list
    """
    match left, right:
        case int(), int():
            return left - right
        case list(), list():
            for lcmp, rcmp in zip(left, right):
                if chk := check_order(lcmp, rcmp):
                    return chk
            return len(left) - len(right)
        case int(), list():
            return check_order([left], right)
        case list(), int():
            return check_order(left, [right])

    # Fallback
    return 1


def calc_valid_sum(packet_pairs: t.Iterable[PACKET_PAIR]) -> int:
    """Calculate the sum of the (1-based) indices of packet pairs that are in the correct order."""
    valid_sum = 0
    for idx, pair in enumerate(packet_pairs, start=1):
        if check_order(*pair) < 0:
            valid_sum += idx

    return valid_sum


def calc_decoder_key(packet_pairs: t.Iterable[PACKET_PAIR]) -> int:
    """
    Calculate the decoder key for the provided packet stream.

    The decoder key is determined by arranging the provided packets in order, then multiplying the
    indices of the divider packets. The incoming packet pair stream is assumed to contain the two
    divider packets (`[2]` and `[6]`)
    """
    # Use chain to flatten our packet pairs iterable before sorting
    # Use cmp_to_key since our comparitor returns integers and not booleans
    organized = sorted(
        itertools.chain.from_iterable(packet_pairs), key=functools.cmp_to_key(check_order)
    )
    return math.prod(idx for idx, packet in enumerate(organized, 1) if packet in [[2], [6]])


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text()

    print(f"Part One: {calc_valid_sum(parse_packets(puzzle_input))}")
    print(f"Part Two: {calc_decoder_key(parse_packets(puzzle_input, insert_divider=True))}")
