import itertools
import typing as t
from collections import defaultdict
from heapq import heappop, heappush
from pathlib import Path


class FileBlock(t.NamedTuple):  # noqa: D101
    id_: int
    n_blocks: int
    n_free: int

    def __str__(self) -> str:
        return f"{str(self.id_)*self.n_blocks}{"."*self.n_free}"


def parse_disk_map(raw_map: str) -> list[FileBlock]:
    """
    Parse the provided disk map into its file block components.

    The disk map uses a dense format to represent the layout of files and free space on disk; the
    digits alternate between indicating the length of a file and the length of free space.

    For example:
        * `12345` would represent would represent a one-block file, two blocks of free space, a
        three-block file, four blocks of free space, and then a five-block file
        * `90909` would represent three nine-block files in a row, with no free space between them

    Each file is given an integer ID number based on the order it appears in the raw disk mapping.
    """
    blocks = []
    for i, b in enumerate(itertools.batched(raw_map, 2)):
        if len(b) == 1:
            # Last block, no free space
            blocks.append(FileBlock(i, int(b[0]), 0))
        else:
            blocks.append(FileBlock(i, int(b[0]), int(b[1])))

    return blocks


def defrag(file_blocks: list[FileBlock]) -> list[int | str]:
    """
    Defragment the disk described by the provided file blocks.

    Each file sector is moved one at a time from the end of the disk to the leftmost free space
    block until there are no gaps remaining between file blocks.

    For example: `0..111....22222` becomes `022111222......`.
    """
    disk_map = []
    for b in file_blocks:
        disk_map.extend(([b.id_] * b.n_blocks) + ["."] * b.n_free)

    swap_pointer = len(disk_map) - 1
    for loc, s in enumerate(disk_map):
        if swap_pointer <= loc:
            # Pointers have met up, so we're done
            break

        if s == ".":
            # Move pointer backwards so we're not shifting empty space
            # Might need to have another guard here if it goes too far?
            while disk_map[swap_pointer] == ".":
                swap_pointer -= 1

            disk_map[loc], disk_map[swap_pointer] = disk_map[swap_pointer], disk_map[loc]
            swap_pointer -= 1

    return disk_map


def defrag_continuous(file_blocks: list[FileBlock]) -> list[int | str]:
    """
    Defragment the disk described by the provided file blocks while maintaining file continuity.

    Each file is attempted to move exactly once in order of decreasing file ID number, starting with
    the file with the highest file ID number. If there is no span of free space to the left of a
    file that is large enough to fit the file, the file does not move.

    For example: `00...111...2...333.44.5555.6666.777.888899` becomes
    `00992111777.44.333....5555.6666.....8888..`
    """
    block_pos = {}
    gaps = defaultdict(list)
    curs = 0
    for b in file_blocks:
        block_pos[b.id_] = curs
        curs += b.n_blocks

        if b.n_free > 0:
            heappush(gaps[b.n_free], curs)
            curs += b.n_free

    disk_size = curs

    for b in file_blocks[:0:-1]:
        block_start = block_pos[b.id_]
        has_gap = False
        for i in range(b.n_blocks, 10):
            if i in gaps:
                has_gap = True
                break

        if not has_gap or not gaps[i]:
            continue

        new_start = heappop(gaps[i])
        block_pos[b.id_] = new_start
        new_gap_size = i - b.n_blocks
        heappush(gaps[new_gap_size], (new_start + b.n_blocks))

    disk_map = ["."] * disk_size
    for b in file_blocks:
        block_start = block_pos[b.id_]
        block_end = block_start + b.n_blocks
        disk_map[block_start:block_end] = [b.id_] * b.n_blocks

    return disk_map


def calculate_checksum(disk_map: list[int | str]) -> int:
    """
    Calculate the checksum for the provided disk mapping.

    The checksum is calculated as the sum of product of each sector position and the file ID number
    it contains. If a sector contains a free space, it is skipped.

    For example, the disk `0.12` has a checksum of `(0*0) + (2*1) + (3*2) = 7`.
    """
    checksum = 0
    for i, v in enumerate(disk_map):
        if isinstance(v, int):
            checksum += i * v

    return checksum


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    parsed_blocks = parse_disk_map(puzzle_input)

    print(f"Part One: {calculate_checksum(defrag(parsed_blocks))}")
    print(f"Part Two: {calculate_checksum(defrag_continuous(parsed_blocks))}")
