from textwrap import dedent

import pytest

from .aoc_2016_day04 import (
    decrypt_room_name,
    is_valid_room,
    parse_room_encryption,
    real_room_sector_sum,
)

SAMPLE_ENCRYPTED_ROOMS = (
    ("aaaaa-bbb-z-y-x-123[abxyz]", "aaaaa-bbb-z-y-x", 123, "abxyz", True),
    ("a-b-c-d-e-f-g-h-987[abcde]", "a-b-c-d-e-f-g-h", 987, "abcde", True),
    ("not-a-real-room-404[oarel]", "not-a-real-room", 404, "oarel", True),
    ("totally-real-room-200[decoy]", "totally-real-room", 200, "decoy", False),
)


@pytest.mark.parametrize(
    ("encrypted", "room_name", "sector_id", "checksum", "truth_is_room"), SAMPLE_ENCRYPTED_ROOMS
)
def test_room_checksum(
    encrypted: str, room_name: str, sector_id: int, checksum: str, truth_is_room: bool
) -> None:
    components = parse_room_encryption(encrypted)

    assert components == (room_name, sector_id, checksum)
    assert is_valid_room(components) is truth_is_room


SAMPLE_ROOM_SPEC = dedent(
    """\
    aaaaa-bbb-z-y-x-123[abxyz]
    a-b-c-d-e-f-g-h-987[abcde]
    not-a-real-room-404[oarel]
    totally-real-room-200[decoy]
    """
)


def test_sector_sum() -> None:
    assert real_room_sector_sum(SAMPLE_ROOM_SPEC) == 1514


def test_name_decryption() -> None:
    encrypted_spec = "qzmt-zixmtkozy-ivhz-343[abcde]"
    components = parse_room_encryption(encrypted_spec)

    assert decrypt_room_name(components) == "very encrypted name"
