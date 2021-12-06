from collections import Counter, deque
from pathlib import Path

FIRST_SPAWN_CYCLE = 8


def spawn_until(starting_ages: list[int], n_days: int) -> int:
    """
    Calculate the total lanternfish population after the provided number of days have elapsed.

    Each lanternfish is assumed to produce a new lanternfish every 7 days, and each new lanternfish
    needs one additional day for its first spawn.
    """
    # Bin the initial population by age & insert into a deque
    age_counts = Counter(starting_ages)
    fish_stock = deque(age_counts.get(n, 0) for n in range(FIRST_SPAWN_CYCLE + 1))
    day = 0
    while day < n_days:
        # Each day we can rotate the deque left, which will rotate the quantity of new lanternfish
        # into the 8 day bin for their first spawn, then the spawning fish can be added into the 7
        # day bin for their next spawn
        fish_stock.rotate(-1)
        fish_stock[6] += fish_stock[-1]
        day += 1

    return sum(fish_stock)


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = [int(age) for age in puzzle_input_file.read_text().strip().split(",")]

    print(f"Part One: {spawn_until(puzzle_input, 80)}")
    print(f"Part Two: {spawn_until(puzzle_input, 256)}")
