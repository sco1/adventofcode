import math
import operator
from pathlib import Path

OPERATORS = [
    sum,
    math.prod,
    min,
    max,
    ...,  # Type 4 is literal values & handled explicitly
    lambda lr: operator.gt(*lr),  # lr assumed to always contain 2 sub-packets
    lambda lr: operator.lt(*lr),  # lr assumed to always contain 2 sub-packets
    lambda lr: operator.eq(*lr),  # lr assumed to always contain 2 sub-packets
]


def hex2bin(in_hex: str) -> str:
    """
    Convert the input hex to its binary representation.

    The resulting binary representation is padded with leading zeros until its length is a multiple
    of four bits.
    """
    binary = f"{int(in_hex, 16):b}"
    return binary.zfill(len(in_hex) * 4)  # Pad with leading zeros


class Transmission:  # noqa: D101
    def __init__(self, raw_hex: str) -> None:
        self.bits = hex2bin(raw_hex)

        self.version_sum = 0
        self._pointer = 0

    def read(self, n_bits: int = 1) -> int:
        """Read the next `n_bits` from the transmission's bit string & cast to an integer."""
        bits = self.bits[self._pointer : (self._pointer + n_bits)]
        self._pointer += n_bits

        return int(bits, 2)


def read_packet(bits_transmission: Transmission) -> int:
    """
    Parse the provided BITS transmission and calculate the sum of its packets' version strings.

    The BITS transmission is assumed to contain a packet at its outermost layer that may itself
    contain many other packets. Every packet begins with a standard header:
        * The first 3 bits encode the packet version
        * The next 3 bits encode the packet type ID

    All numbers encoded in any packet are represented as binary with the most significant bit
    first.

    Packets with a type ID 4 represent a literal value. To do this, the binary number is padded
    with leading zeroes until its length is a multiple of four bits, and then it is broken into
    groups of four bits. Each group is prefixed by a 1 bit except the last group, which is
    prefixed by a 0 bit. These groups of five bits immediately follow the packet header.

    Every other type of packet represents an operator that performs some calculation on one or
    more sub-packets contained within. An operator packet contains one or more packets. To
    indicate which subsequent binary data represents its sub-packets, an operator packet can use
    one of two modes indicated by the bit immediately after the packet header; this is called
    the length type ID:
        * If the length type ID is 0, then the next 15 bits are a number that represents the
        total length in bits of the sub-packets contained by this packet
        * If the length type ID is 1, then the next 11 bits are a number that represents the
        number of sub-packets immediately contained by this packet

    Finally, after the length type ID bit and the 15-bit or 11-bit field, the sub-packets
    appear.
    """
    bits_transmission.version_sum += bits_transmission.read(3)
    type_id = bits_transmission.read(3)

    # Literal value short-circuits
    if type_id == 4:
        literal = 0
        while True:
            # When the first bit is 0, then we have the last group
            continue_bit = bits_transmission.read()

            # We're bit shifting to the left as we assemble the groups
            literal = (literal << 4) + bits_transmission.read(4)
            if not continue_bit:
                return literal

    # All other type IDs represent operators
    length_id = bits_transmission.read()
    sub_packets = []
    if length_id:
        # The next 11 bits represent the number of sub-packets
        n_sub = bits_transmission.read(11)
        for _ in range(n_sub):
            sub_packets.append(read_packet(bits_transmission))
    else:
        # The next 15 bits represent the total length, in bits, of the sub-packets in this packet
        sub_length = bits_transmission.read(15)
        last_sub_bit = bits_transmission._pointer + sub_length
        while bits_transmission._pointer < last_sub_bit:
            sub_packets.append(read_packet(bits_transmission))

    return int(OPERATORS[type_id](sub_packets))


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    bits_transmission = Transmission(puzzle_input)
    val = read_packet(bits_transmission)
    print(f"Part One: {bits_transmission.version_sum}")
    print(f"Part Two: {val}")
