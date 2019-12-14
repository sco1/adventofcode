from pathlib import Path

import numpy as np


def load_image(raw_stream: str, width: int, height: int) -> np.ndarray:
    """Reshape the provided stream of integers (as str) into a n x width x height array of int."""
    return np.fromiter(raw_stream, dtype=int).reshape(-1, height, width)


def check_image(image: np.ndarray) -> int:
    """
    Check image for corruption.

    Image is checked by finding the layer with the fewest occurrence of 0 & multiplying the number
    of instances of 1 by the number of instances of 2
    """
    zero_counts = np.count_nonzero(image == 0, axis=2).sum(axis=1)
    min_location = np.argmin(zero_counts)

    return np.sum(image[min_location, :, :] == 1) * np.sum(image[min_location, :, :] == 2)


def merge_layers(image: np.ndarray) -> np.ndarray:
    """Merge image into a single layer."""
    # Find first index along the "columns" of layers where pixel value is not 2
    # Use expand_dims so we can use with take_along_axis
    idx = np.expand_dims(np.argmax(image != 2, axis=0), axis=0)

    # Use indices to pick the pixel values from the indexed slice
    return np.squeeze(np.take_along_axis(image, idx, axis=0))


def show_merged_image(image: np.ndarray) -> None:
    """
    Print the provided image to the console.

    Array is assumed to contain binary integers.
    """
    height, width = image.shape
    str_image = [["  " for _ in range(width)] for _ in range(height)]

    for (y, x), value in np.ndenumerate(image):
        if value == 1:
            str_image[y][x] = "##"

    print("\n".join("".join(i) for i in str_image))


if __name__ == "__main__":
    puzzle_input = Path("./puzzle_input.txt")

    with puzzle_input.open("r") as f:
        encoded_image = f.read().strip()

    width = 25
    height = 6
    decoded_image = load_image(encoded_image, width=width, height=height)

    # Part 1
    print(check_image(decoded_image))

    # Part 2
    merged_image = merge_layers(decoded_image)
    show_merged_image(merged_image)
