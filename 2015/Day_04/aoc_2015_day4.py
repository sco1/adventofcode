import hashlib
from pathlib import Path


def mine_adventcoin(
    secret_key: str, valid_hash_prefix: str = "00000", max_iter: int = 100000000
) -> int:
    """
    Mine some AdventCoin for Santa!

    Return the lowest integer that, when combined with `secret_key`, produces a valid MD5 hash.

    Hashes are valid if they are prefixed with `valid_hash_prefix`.

    `max_iter` can optionally be specified (default = 100,000,000) to keep the miner from looping
    indefinitely.
    """
    for ii in range(max_iter):
        message = f"{secret_key}{ii}".encode()  # Encode to bytestring for hashing
        if hashlib.md5(message).hexdigest().startswith(valid_hash_prefix):
            return ii


puzzle_input_file = Path("./puzzle_input.txt")
with puzzle_input_file.open(mode="r") as f:
    puzzle_input = f.read()

print(mine_adventcoin(puzzle_input))
print(mine_adventcoin(puzzle_input, valid_hash_prefix="000000"))
