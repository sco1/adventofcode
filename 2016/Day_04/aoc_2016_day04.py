import re
from collections import Counter, namedtuple
from pathlib import Path

ENCRYPTION_SPEC = re.compile(r"([a-z-]+)-(\d+)\[([a-z]+)\]")
RoomComp = namedtuple("RoomComp", ("name", "sector_id", "checksum"))


def parse_room_encryption(encrypted: str) -> RoomComp:
    """
    Parse the provided room encryption into its components.

    An encrypted room string consists of an encrypted name (lowercase letters separated by dashes)
    followed by a dash, a sector ID, and a checksum in square brackets.

    e.g. `aaaaa-bbb-z-y-x-123[abxyz]`
    """
    comps = ENCRYPTION_SPEC.findall(encrypted)[0]
    if not comps:
        raise ValueError(f"Could not parse room encryption: '{encrypted}'")

    room_name, sector_id, checksum = comps
    return RoomComp(room_name, int(sector_id), checksum)


def is_valid_room(room_components: RoomComp) -> bool:
    """
    Determine if a room is real.

    A room is real (not a decoy) if the checksum is the five most common letters in the encrypted
    name, in order, with ties broken by alphabetization.

    e.g. `not-a-real-room-404[oarel]` is a real room and `totally-real-room-200[decoy]` is not.
    """
    counts = Counter(sorted(room_components.name.replace("-", "")))
    computed_checksum = "".join(element[0] for element in counts.most_common(5))

    return computed_checksum == room_components.checksum


def real_room_sector_sum(room_list: str) -> int:  # noqa: D103
    sector_sum = 0
    for room in room_list.strip().splitlines():
        room_comp = parse_room_encryption(room)
        if is_valid_room(room_comp):
            sector_sum += room_comp.sector_id

    return sector_sum


def decrypt_room_name(room_components: RoomComp) -> str:
    """
    Decrypt the specified room name assuming it's been encrypted by a shift cipher.

    A room name is decrypted by rotating each letter forward through the alphabet a number of times
    equal to the room's sector ID. `A` becomes `B`, `B` becomes `C`, `Z` becomes `A`, and so on.
    Dashes become spaces.
    """
    decrypted_letters = []
    for letter in room_components.name:
        if letter == "-":
            decrypted_letters.append(" ")
        else:
            decrypted_letters.append(
                chr((((ord(letter) - 97) + room_components.sector_id) % 26) + 97)
            )

    return "".join(decrypted_letters)


def join_decrypted_room_names(room_list: str) -> str:  # noqa: D103
    decrypted = []
    for room in room_list.strip().splitlines():
        room_comp = parse_room_encryption(room)
        decrypted.append(f"{room_comp.sector_id}: {decrypt_room_name(room_comp)}")

    return "\n".join(decrypted)


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text()

    print(f"Part One: {real_room_sector_sum(puzzle_input)}")
    print(f"Part Two:\n{join_decrypted_room_names(puzzle_input)}")
