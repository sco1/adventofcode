from pathlib import Path
from typing import List


def calculate_side_surface_areas(length: int, width: int, height: int) -> List[int]:
    """
    Calculate the surface area of each unique side of a rectangular prism with the input dimensions.

    Return a sorted list of the surface areas of the 3 unique sides
    """
    return sorted([length * width, length * height, width * height])


def calculate_present_volume(length: int, width: int, height: int) -> int:
    """Calculate the volume of a present, assuming a rectangular prism with the given dimensions"""
    return length * width * height


def calculate_side_perimeters(length: int, width: int, height: int) -> List[int]:
    """
    Calculate the perimeter of each unique side of a rectangular prism with the input dimensions.

    Return a sorted list of the perimeters of the 3 unique sides
    """
    return sorted([2 * (length + width), 2 * (length + height), 2 * (width + height)])


def calculate_present_wrapping_paper(length: int, width: int, height: int) -> int:
    """
    Calculate the square footage of wrapping paper needed to wrap the present.

    The present is assumed to be a rectangular prism with the input dimensions. Wrapping paper
    square footage is calculated as the surface area of the present plus the surface area of the
    smallest side as wiggle room.
    """
    surface_areas = calculate_side_surface_areas(length, width, height)

    # Total surface area is 2x each side
    total_surface_area = sum([side * 2 for side in surface_areas])
    total_surface_area += surface_areas[0]  # Add in wiggle room

    return total_surface_area


def calculate_present_ribbon(length: int, width: int, height: int) -> int:
    """
    Calculate the total length of ribbon needed to wrap the present.

    The present is assumed to be a rectangular prism with the input dimensions. Ribbon length is
    calculated as the perimeter of the smallest side of the present plus a length equal to the
    present's volume as the length required to make a bow.
    """
    perimeters = calculate_side_perimeters(length, width, height)
    volume = calculate_present_volume(length, width, height)

    return perimeters[0] + volume


def calculate_total_wrapping_paper(present_dimensions: List[List[int]]) -> int:
    """
    Calculate the total square footage of wrapping paper required to wrap all of the presents.

    `present_dimensions` is assumed to be a list of lists of the present dimensions (lxwxh)
    """
    total_wrapping_paper = 0
    for present in present_dimensions:
        length, width, height = present
        total_wrapping_paper += calculate_present_wrapping_paper(length, width, height)

    return total_wrapping_paper


def calculate_total_ribbon(present_dimensions: List[List[int]]) -> int:
    """
    Calculate the total length of ribbon required to wrap all of the presents.

    `present_dimensions` is assumed to be a list of lists of the present dimensions (lxwxh)
    """
    total_ribbon = 0
    for present in present_dimensions:
        length, width, height = present
        total_ribbon += calculate_present_ribbon(length, width, height)

    return total_ribbon


puzzle_input_file = Path("./puzzle_input.txt")
with puzzle_input_file.open(mode="r") as f:
    puzzle_input = [[int(dim) for dim in line.split("x")] for line in f]

print(calculate_total_wrapping_paper(puzzle_input))
print(calculate_total_ribbon(puzzle_input))
