import re
import typing as t
from pathlib import Path

import numpy as np

CLAIM_RE = re.compile(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)")


class Claim(t.NamedTuple):  # noqa: D101
    claim_id: int
    left_edge: int
    top_edge: int
    width: int
    height: int


def _parse_claims(raw_claims: list[str]) -> list[Claim]:
    """
    Parse the provided cloth claims into their dimensional components.

    Claims are assumed to be of the form:
        * `#<int> @ <int>,<int>: <int>x<int>`

    Each claim's rectangle is defined as follows:
        * Inches between the left edge of the fabric and the left edge of the rectangle
        * Inches between the top edge of the fabric and the top edge of the rectangle
        * The width of the rectangle in inches
        * The height of the rectangle in inches
    """
    parsed_claims = []
    for claim in raw_claims:
        components = CLAIM_RE.findall(claim)[0]
        parsed_claims.append(Claim(*(int(component) for component in components)))

    return parsed_claims


def _find_cloth_size(claims: list[Claim]) -> tuple:
    """Calculate the bottom right coordinates of the box bounding the provided claims."""
    max_left = max((claim.left_edge for claim in claims))
    max_top = max((claim.top_edge for claim in claims))
    max_width = max((claim.width for claim in claims))
    max_height = max((claim.height for claim in claims))

    return (max_left + max_width), (max_top + max_height)


def _build_cloth(claims: list[Claim]) -> np.ndarray:
    """Build an array representing the provided claims on the cloth to be cut."""
    cloth_dims = _find_cloth_size(claims)
    cloth = np.zeros(cloth_dims)

    for claim in claims:
        row_indices = (claim.top_edge, (claim.top_edge + claim.height))
        column_indices = (claim.left_edge, (claim.left_edge + claim.width))

        cloth[row_indices[0] : row_indices[1], column_indices[0] : column_indices[1]] += 1

    return cloth


def calculate_overlap(cloth: np.ndarray) -> int:
    """Calculate the square inches of cloth covered by more than one claim."""
    return np.count_nonzero(cloth > 1)


def find_nonoverlapping_claim(cloth: np.ndarray, claims: list[Claim]) -> int:
    """
    Identify the fabric claim that contains no overlap with any other claim.

    NOTE: It is assumed that there is exactly one non-overlapping claim in the provided claims.
    """
    # The non-overlapping claim will describe a subarray where all values are 1
    for claim in claims:
        row_indices = (claim.top_edge, (claim.top_edge + claim.height))
        column_indices = (claim.left_edge, (claim.left_edge + claim.width))

        subarray = cloth[row_indices[0] : row_indices[1], column_indices[0] : column_indices[1]]
        if np.all(subarray == 1):
            return claim.claim_id

    raise ValueError("No non-overlapping claim found.")


if __name__ == "__main__":
    puzzle_input_file = Path("puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().splitlines()

    claims = _parse_claims(puzzle_input)
    cloth = _build_cloth(claims)

    print(f"Part One: {calculate_overlap(cloth)}")
    print(f"Part Two: {find_nonoverlapping_claim(cloth, claims)}")
