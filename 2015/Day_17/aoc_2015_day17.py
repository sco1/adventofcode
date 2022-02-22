from itertools import combinations
from pathlib import Path


def containers_for_volume(
    container_pool: list[int], target_volume: int = 150, minimize: bool = False
) -> int:
    """
    Calculate the number of container combinations that yield the specified total volume.

    If the `minimize` flag is set the count is instead the number of combinations of the minimum
    possible number of containers.
    """
    n_containers = len(container_pool)
    min_containers = n_containers
    valid_combinations = []
    for pick_n in range(1, n_containers + 1):
        for combo in combinations(container_pool, pick_n):
            combo_vol = sum(combo)
            if combo_vol == target_volume:
                if not minimize:
                    valid_combinations.append(combo)
                else:
                    if len(combo) < min_containers:
                        valid_combinations = [combo]
                        min_containers = len(combo)
                    elif len(combo) == min_containers:
                        valid_combinations.append(combo)

    return len(valid_combinations)


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().splitlines()

    containers = [int(line) for line in puzzle_input]
    print(f"Part One: {containers_for_volume(containers)} valid combinations")
    print(f"Part Two: {containers_for_volume(containers, minimize=True)} containers")
