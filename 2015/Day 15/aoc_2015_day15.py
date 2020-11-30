import typing as t
from itertools import product
from math import prod
from pathlib import Path


class Ingredient(t.NamedTuple):
    """Represent a cookie ingredient & its property factors."""

    name: str
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int

    @classmethod
    def from_puzzle_input(cls, puzzle_input_line: str):
        """
        Generate an instance from a line of the puzzle input.

        Input lines are of the form:
            "Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8"
        """
        ingredient_name, _, properties = puzzle_input_line.partition(":")

        parsed_properties = {
            prop_name: int(prop_val)
            for prop in properties.split(",")
            for prop_name, prop_val in (prop.split(),)
        }

        return cls(ingredient_name, **parsed_properties)


class Recipe:
    """Represent a holiday cookie recipe & its optimization methods."""

    def __init__(self, ingredients: list[Ingredient]):
        self.ingredients = {ingredient.name: ingredient for ingredient in ingredients}
        self.n_ingredients = len(self.ingredients)

    @classmethod
    def from_puzzle_input(cls, puzzle_input: list[str]):
        """Build a recipe using the list of ingredients provided by the puzzle input."""
        return cls([Ingredient.from_puzzle_input(line) for line in puzzle_input])

    def optimize_measurements(self, calorie_target: t.Optional[int] = None) -> int:
        """
        Determine the combination of ingredient quantities to maximize the recipe's score.

        The total score of the recipe is found by adding up each of the properties and then
        multiplying together everything except calories. Properties are provided per-tablespoon.

        If a property score ends up negative, the score becomes 0.

        A calorie target may be optionally specified to ignore any recipes that don't yield a recipe
        whose calorie count doesn't exactly match the target.
        """
        max_score = 0

        max_volume = 100
        for measurements in product(range(max_volume + 1), repeat=self.n_ingredients):
            # Use max_volme + 1 to allow for ingredient quantities of 100
            if sum(measurements) > max_volume:
                continue

            # If set, check whether we've met the calorie target before continuing
            if calorie_target is not None:
                calories = sum(
                    ingredient.calories * property_factor
                    for property_factor, ingredient in zip(measurements, self.ingredients.values())
                )

                if calories != calorie_target:
                    continue

            ingredient_scores = [
                sum(
                    ingredient[n] * property_factor
                    for property_factor, ingredient in zip(measurements, self.ingredients.values())
                )
                for n in range(1, 5)  # Skip name & calories in the Ingredient NamedTuple
            ]

            # Scores <= 0 will result in a max_score of 0, which we can skip
            if any(subscore <= 0 for subscore in ingredient_scores):
                continue

            score = prod(ingredient_scores)
            if score > max_score:
                max_score = score

        return max_score


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().splitlines()

    recipe = Recipe.from_puzzle_input(puzzle_input)
    print(f"Part 1 Max Score: {recipe.optimize_measurements()}")
    print(f"Part 2 Max Score: {recipe.optimize_measurements(calorie_target=500)}")
