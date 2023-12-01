import hashlib
import itertools
from collections import abc
from pathlib import Path


def password_hashes(door_id: str) -> abc.Generator[str, None, None]:
    """
    Yield password characters using the provided door ID as a seed.

    The MD5 hash indicates the next character in the password if its hexadecimal representation
    starts with five zeroes. If it does, the sixth character in the hash is the next character of
    the password.
    """
    for idx in itertools.count():
        hashed = hashlib.md5(f"{door_id}{idx}".encode("ascii")).hexdigest()
        if hashed.startswith("00000"):
            yield hashed


def calculate_door_password(door_id: str, password_length: int = 8) -> str:
    """
    Determine the password for a door with the given ID.

    The password for the door is generated one character at a time by finding the MD5 hash of the
    door ID and an increasing integer index (starting with 0). A hash indicates the next character
    in the password if its hexadecimal representation starts with five zeroes.

    If it does, the sixth character in the hash is the next character of the password.
    """
    hash_gen = password_hashes(door_id)
    hashes = [next(hash_gen) for _ in range(password_length)]

    return "".join(hash[5] for hash in hashes)


def calculate_door_password_positional(door_id: str, password_length: int = 8) -> str:
    """
    Determine the password for a door with the given ID.

    The password for the door is generated one character at a time by finding the MD5 hash of the
    door ID and an increasing integer index (starting with 0). A hash indicates the next character
    in the password if its hexadecimal representation starts with five zeroes.

    If it does, the seventh character of the hash is the next password character and the sixth
    character, if it's a valid index, represents its position in the password. If the sixth
    character does not represent a valid position, the hash is ignored and and we move on to
    consider the next valid hash.
    """
    hash_gen = password_hashes(door_id)
    components = [""] * password_length
    n_found = 0
    while True:
        next_hash = next(hash_gen)

        try:
            idx, c = int(next_hash[5]), next_hash[6]
        except ValueError:
            continue

        if (idx not in range(password_length)) or components[idx]:
            continue
        else:
            components[idx] = c
            n_found += 1

        if n_found == password_length:
            return "".join(components)


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    print(f"Part One: {calculate_door_password(puzzle_input)}")
    print(f"Part Two: {calculate_door_password_positional(puzzle_input)}")
