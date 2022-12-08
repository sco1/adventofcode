from pathlib import Path

import numpy as np


def parse_tree_map(puzzle_input: str) -> np.ndarray:
    """
    Parse the provided tree height map into an array.

    Each tree in the map is assumed to be represented as a single digits whose value is its height,
    where `0` is the shortest and `9` is the tallest.
    """
    return np.genfromtxt(puzzle_input.splitlines(), dtype=np.uint8, delimiter=1)


def count_visible_trees(tree_map: np.ndarray) -> int:
    """
    Count the number of trees that are visible from outside the grid along at least one edge.

    It is assumed that the onlooker is only looking along a row or a column. A tree is visible if
    all of the other trees between it and an edge of the grid are shorter than it.
    """
    visible_dirs = np.zeros_like(tree_map)
    for _ in range(4):  # Just rotate the grid for each direction to simplify the code
        # For each tree, cast a ray rightward and see if it gets to the edge of the grid
        for (y, x), query_height in np.ndenumerate(tree_map):
            is_lower = (tree < query_height for tree in tree_map[y, x + 1 :])
            visible_dirs[y, x] |= all(is_lower)  # Use OR to keep any True values once we've rotated

        tree_map = np.rot90(tree_map)
        visible_dirs = np.rot90(visible_dirs)

    return visible_dirs.sum()


def find_max_scenic_score(tree_map: np.ndarray) -> int:
    """
    Find the highest scoring viewing distance for the provided tree map.

    To measure the viewing distance from a given tree, look up, down, left, and right from that
    tree, stopping if an edge is reached or at the first tree that is the same height or taller than
    the tree under consideration.

    A tree's scenic score is found by multiplying together its viewing distance in each of the four
    directions.
    """
    tree_score = np.ones_like(tree_map, dtype=int)  # Need more than 8 bits for this part
    for _ in range(4):  # Just rotate the grid for each direction to simplify the code
        for (y, x), query_height in np.ndenumerate(tree_map):
            dist_to_edge = tree_map.shape[-1] - x - 1  # Value if we can see to the edge
            is_blocking = (tree >= query_height for tree in tree_map[y, x + 1 :])

            # We want the index of the first tree that blocks the view, or the edge of the grid
            tree_score[y, x] *= next(
                (dist + 1 for dist, blocking_tree in enumerate(is_blocking) if blocking_tree),
                dist_to_edge,
            )

        tree_map = np.rot90(tree_map)
        tree_score = np.rot90(tree_score)

    return tree_score.max()


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text()

    tree_map = parse_tree_map(puzzle_input)
    print(f"Part One: {count_visible_trees(tree_map)}")
    print(f"Part Two: {find_max_scenic_score(tree_map)}")
