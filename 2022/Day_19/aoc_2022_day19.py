import re
import typing as t
from pathlib import Path

TYPE_RE = re.compile(r"(\w+) robot")
COMPONENT_RE = re.compile(r"(\d+) (\w+)")

MATERIALS: t.TypeAlias = dict[str, int]
BLUEPRINT_COST: t.TypeAlias = dict[str, MATERIALS]
BLUEPRINT: t.TypeAlias = tuple[int, BLUEPRINT_COST]


def parse_blueprints(raw_blueprints: str) -> list[BLUEPRINT]:
    """
    Parse the provided blueprints into an enumerated construction specification.

    One blueprint is assumed to be provided on each line of the input. Blueprints are assumed to be
    of the following form:

    ```
    Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 4 ore.
    Blueprint 2: Each ore robot costs 3 ore. Each clay robot costs 4 ore.
    ```

    Each blueprint is contains one or more robot construction specifications, delimited by `.`. Each
    construction spec contains one or more ore requirements, specified as `<quantity> <type>`.
    """
    blueprints = []
    for blueprint in raw_blueprints.splitlines():
        bp_label, robots = blueprint.split(":")
        bp_id = int(re.findall(r"\d+", bp_label)[0])

        costs = {}
        for robot in robots.split("."):
            if not robot:
                continue

            robot_type = TYPE_RE.findall(robot)[0]
            components = {rock_type: int(count) for count, rock_type in COMPONENT_RE.findall(robot)}

            costs[robot_type] = components

        blueprints.append((bp_id, costs))

    return blueprints


def _can_build(robot_cost: MATERIALS, inventory: MATERIALS) -> bool:
    return all(inventory.get(material, 0) >= need for material, need in robot_cost.items())


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text()

    blueprints = parse_blueprints(puzzle_input)
    print(f"Part One: {...}")
    print(f"Part Two: {...}")
