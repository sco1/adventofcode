import pytest

from .aoc_2021_day16 import Transmission, hex2bin, read_packet

HEX_BIN_TESTS = [
    ("D2FE28", "110100101111111000101000"),
    ("38006F45291200", "00111000000000000110111101000101001010010001001000000000"),
    ("EE00D40C823060", "11101110000000001101010000001100100000100011000001100000"),
]


@pytest.mark.parametrize(("in_hex", "truth_binary"), HEX_BIN_TESTS)
def test_hex2bin(in_hex: str, truth_binary: str) -> None:
    assert hex2bin(in_hex) == truth_binary


VERSION_SUM_TESTS = [
    ("D2FE28", 6),
    ("38006F45291200", 9),
    ("EE00D40C823060", 14),
    ("8A004A801A8002F478", 16),
    ("620080001611562C8802118E34", 12),
    ("C0015000016115A2E0802F182340", 23),
    ("A0016C880162017C3686B18A3D4780", 31),
]


@pytest.mark.parametrize(("in_hex", "truth_version_sum"), VERSION_SUM_TESTS)
def test_part_one(in_hex: str, truth_version_sum: int) -> None:
    bits_transmission = Transmission(in_hex)
    read_packet(bits_transmission)
    assert bits_transmission.version_sum == truth_version_sum


OPERATOR_TESTS = [
    ("C200B40A82", 3),
    ("04005AC33890", 54),
    ("880086C3E88112", 7),
    ("CE00C43D881120", 9),
    ("D8005AC2A8F0", 1),
    ("F600BC2D8F", 0),
    ("9C005AC2F8F0", 0),
    ("9C0141080250320F1802104A08", 1),
]


@pytest.mark.parametrize(("in_hex", "truth_result"), OPERATOR_TESTS)
def test_part_two(in_hex: str, truth_result: int) -> None:
    bits_transmission = Transmission(in_hex)
    assert read_packet(bits_transmission) == truth_result
