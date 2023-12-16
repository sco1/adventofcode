import re
import typing as t
from collections import defaultdict
from pathlib import Path

LENS_SPEC = re.compile(r"(\w+)(=|-)(\d*)")
BOX_T: t.TypeAlias = list[tuple[str, int]]


def hash_val(hash: str) -> int:
    """
    Calculate the value of the provided hash.

    From a starting value of `0`, for each character in the provided hash:
        * Increase the current value by the character's ASCII value
        * Multiply the current value by `17`
        * Set the current value to the remainder of the current value divided by `200`
    """
    val = 0
    for c in hash:
        val += ord(c)
        val *= 17
        val %= 256

    return val


def _find_lens(box: BOX_T, label: str) -> int | None:
    """Find the slot location of the first matching lens in the provided box."""
    for idx, (lens, _) in enumerate(box):
        if lens == label:
            return idx

    # No lens found with this label
    return None


def bin_lenses(steps: str) -> dict[int, BOX_T]:
    """
    Slot lenses into their box locations according to the provided steps.

    Slotting steps are provided as a comma separated list of hash sequences of the form:
    <label><operation><focal length>, where the label is assumed to be one or more ASCII characters,
    operation is either `-` or `=`, and focal length is an integer. Sequences with a `-` operation
    will not contain a focal length. For example: `rn=1` has the label `rn`, operation `=`, and
    focal length `1`, and `qp-` has the label `qp` and operation `-`.

    The box ID for each step is calculated as the output of the facility's hashing algorithm.

    The action taken for each step is dispatched based on its operator:
        * For `-`, remove the lens with the specified label from the box, moving any remaining
        lenses forward without changing their order
        * For `=`, if there is already a lens in the box with the same label, replace the old lens
        with the new one, without making any changes to lens order. If a lens with the same label is
        not present, slot the lens immediately after any existing lenses in the box.
    """
    # A linked list may be better than list but this seems good enough
    boxes: dict[int, BOX_T] = defaultdict(list)
    for step in steps.split(","):
        comps = LENS_SPEC.findall(step)[0]
        label, op = comps[0], comps[1]
        box_id = hash_val(label)
        focal_length = int(comps[2]) if comps[2] else None

        lens_idx = _find_lens(boxes[box_id], label)
        if op == "-":
            if lens_idx is not None:
                boxes[box_id].pop(lens_idx)
        elif op == "=":
            if focal_length is None:
                raise ValueError("Lens addition step must contain a focal lengh spec.")

            if lens_idx is None:
                boxes[box_id].append((label, focal_length))
            else:
                boxes[box_id][lens_idx] = (label, focal_length)
        else:
            raise ValueError(f"Unknown operator: '{op}'")

    return boxes


def calculate_focusing_power(boxes: dict[int, BOX_T]) -> int:
    """
    Calculate the total focusing power of the lens boxes.

    The focusing power of each lens is calculated by multiplying together:
        * 1 + box number
        * Lens location within the box (1-indexed)
        * Focal length of the lens
    """
    focusing_power = 0
    for box_id, lenses in boxes.items():
        for slot_idx, (_, focal_length) in enumerate(lenses, start=1):
            focusing_power += (box_id + 1) * slot_idx * focal_length

    return focusing_power


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    print(f"Part One: {sum(hash_val(h) for h in puzzle_input.split(','))}")

    boxes = bin_lenses(puzzle_input)
    print(f"Part Two: {calculate_focusing_power(boxes)}")
