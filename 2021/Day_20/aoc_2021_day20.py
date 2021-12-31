from pathlib import Path

import numpy as np
from scipy import signal

# To get the 9-bit index out of our convolution, we need our kernel to map to the appropriate bits;
# Since the kernel is flipped when the convolution is applied, the most significant bit will be at
# the bottom left, giving us our bits:
#     2 ** [ 1 2 3
#            4 5 6
#            7 8 9 ]
KERNEL = 2 ** (np.arange(9).reshape((3, 3)))


def parse_input(puzzle_input: str) -> tuple[np.array, np.array]:
    """
    Parse the provided puzzle input into its algorithm and image components.

    The algorithm and image components are assumed to be delimited by a blank line. The algorithm is
    assumed to be contained on a single line and the image is assumed to be one or more lines. The
    components are assumed to be strings, where `"."` is `0` and `"#"` is `1`; the components are
    converted into binary numpy arrays.
    """
    raw_algo, raw_image = puzzle_input.split("\n\n")

    algorithm = np.fromiter((c == "#" for c in raw_algo), dtype=bool)
    # Couldn't figure out how to get the nested iterator to work with fromiter without making a
    # monstrosity
    image = np.array([[c == "#" for c in row] for row in raw_image.splitlines()], dtype=bool)

    return algorithm, image


def enhance_image(image: np.ndarray, algorithm: np.ndarray, n_iter: int) -> int:
    """
    Run the specified number of iterations of our image enhancement program.

    Each pixel of the output image is determined by looking at a 3x3 square of pixels centered on
    the corresponding input image pixel. These nine input pixels are combined into a single binary
    number that is used as an index into the image enhancement algorithm string.

    The image enhancement algorithm is assumed to be length `512`, enough to match every possible
    9-bit binary number.
    """
    fill = False
    for i in range(n_iter):
        # Perform the convolution, then use the values to index into the enhancement algorithm to
        # get the enhanced image
        image = algorithm[signal.convolve2d(image, KERNEL, fillvalue=fill)]

        # In a demonic twist for today's puzzle, we need to be aware or our fill value and the first
        # value of our enhancement algorithm. If our padding is all False & the first value of the
        # enhancement algorithm (all False gives us a binary index 0) is True, then we end up
        # turning on all of the padding pixels. If this happens, we need to flip the other way for
        # the next iteration or we'll end up miscalculating the enhancement.
        #
        # Thanks to this comment chain for helping me figure out why the convolution was working for
        # the example & not for my puzzle input:
        #     https://www.reddit.com/r/adventofcode/comments/rkf5ek/comment/hp9h92j/
        fill = algorithm[0] and not (i % 2)

    return np.sum(image)


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()
    algorithm, image = parse_input(puzzle_input)

    print(f"Part One: {enhance_image(image, algorithm, 2)}")
    print(f"Part Two: {enhance_image(image, algorithm, 50)}")
