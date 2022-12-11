from __future__ import annotations

import math
import operator
import re
import typing as t
from collections import deque
from functools import partial
from pathlib import Path

TEST_TUPLE: t.TypeAlias = tuple[int, int, int]


class MonkeyGame:  # noqa: D101
    _inspect_count: list[int]
    _lcm = int

    def __init__(
        self,
        items: list[deque[int]],
        operations: list[t.Callable[[int], int]],
        tests: list[TEST_TUPLE],
        inspection_relief: bool = True,
    ) -> None:
        """
        Create a game instance using the provided parameters.

        `items` is assumed to be a list of worry levels for each item in their respective monkey's
        posession.

        `operations` is assumed to contain a callable for each monkey to model its affect on an
        item's worry level after it's inspected by the monkey.

        `tests` is assumed to contain the test parameters used by each monkey to decide where to
        throw each item after inspection.

        If `inspection_relief` is `True`, the item's worry level is divided by 3 following the
        monkey's inspection.
        """
        self.items = items
        self.operations = operations
        self.tests = tests
        self.inspection_relief = inspection_relief

        self._inspect_count = [0] * len(items)
        self._lcm = math.lcm(*(test[0] for test in tests))  # Need this for Pt 2 to prevent overflow

    def run_n(self, n_rounds: int = 1) -> None:
        """
        Run `n_rounds` of the monkey game.

        For each round of the monkey game, each monkey takes a turn. For each item in the monkey's
        posession at the beginning of their turn:
            1. The monkey inspects the item, adjusting its worry level using its respective
            operation
            2. If `inspection_relief` is `True`, the item's worry level is divided by 3 and rounded
            down to the nearest integer
            3. The new worry value is checked against the monkey's test function, determining which
            monkey to throw the item to

        A monkey's turn ends when all its items have been thrown. Any thrown items go to the end of
        the receiving monkey's inventory. Therefore, a monkey that starts a round with no items
        could end up inspecting and throwing many items by the time its turn comes around.
        """
        for _ in range(n_rounds):
            for monkey, items in enumerate(self.items):
                while items:
                    val = items.popleft()
                    self._inspect_count[monkey] += 1
                    val = self.operations[monkey](val)
                    if self.inspection_relief:
                        val = val // 3
                    else:
                        # If we're not arbitrarily truncating the value then we need to use another
                        # method to keep the values bounded while retaining their relative meaning,
                        # otherwise we're going to overflow as the number of rounds gets higher
                        val = val % self._lcm

                    div_val, true_target, false_target = self.tests[monkey]
                    if val % div_val == 0:
                        self.items[true_target].append(val)
                    else:
                        self.items[false_target].append(val)

    def _worry_test(self, item: int, cond_val: int, if_true: int, if_false: int) -> None:
        if item % cond_val == 0:
            self.items[if_true].append(item)
        else:
            self.items[if_false].append(item)

    @property
    def monkey_business(self) -> int:
        """
        Calculate the monkey business for the current state of the monkey game.

        Monkey business is calculated as the product of the 2 highest monkey inspection counts.
        """
        a, b, *_ = sorted(self._inspect_count, reverse=True)
        return a * b

    @classmethod
    def from_notes(cls, raw_notes: str, inspection_relief: bool = True) -> MonkeyGame:
        """
        Parse the game parameters from the provided notes.

        Parameters are assumed to be provided in the following form:

        ```
        Monkey 0:
        Starting items: 79, 98
        Operation: new = old * 19
        Test: divisible by 23
            If true: throw to monkey 2
            If false: throw to monkey 3
        ```
        """
        items = []
        operations = []
        tests = []

        for monkey in raw_notes.split("\n\n"):
            _, starting, operation, *test = monkey.splitlines()
            items.append(deque(int(item) for item in re.findall(r"\d+", starting)))
            operations.append(_map_operation(operation.partition(":")[-1].strip()))
            tests.append(_map_test(test))

        return cls(items, operations, tests, inspection_relief)

    def __str__(self) -> str:
        """Prints the current item summary."""
        return "\n".join(f"Monkey {n}: {items}" for n, items in enumerate(self.items))


def _map_operation(raw_operation: str) -> t.Callable:
    operation = raw_operation.partition("=")[-1].strip()
    match operation.split():
        case ("old", "*", "old"):
            return partial(pow, exp=2)
        case ("old", "*", factor):
            return partial(operator.mul, int(factor))
        case ("old", "+", "old"):
            return partial(operator.mul, 2)
        case ("old", "+", factor):
            return partial(operator.add, int(factor))
        case _:
            raise ValueError(f"Unknown operation: '{operation}'")


def _map_test(raw_test: list[str]) -> TEST_TUPLE:
    cond_val, true_target, false_target = (
        int(val) for line in raw_test for val in re.findall(r"\d+", line)
    )

    return cond_val, true_target, false_target


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text()

    game = MonkeyGame.from_notes(puzzle_input)
    game.run_n(20)

    print(f"Part One: {game.monkey_business}")

    game = MonkeyGame.from_notes(puzzle_input)
    game.run_n(10_000)
    print(f"Part Two: {game.monkey_business}")
