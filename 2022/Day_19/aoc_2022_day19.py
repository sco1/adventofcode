import re
from pathlib import Path

TYPE_RE = re.compile(r"(\w+) robot")
COMPONENT_RE = re.compile(r"(\d+) (\w+)")


def parse_blueprints(raw_blueprints: str) -> list:
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


def _can_build(blueprint: dict, materials: dict) -> bool:
    return all(materials.get(material, 0) >= need for material, need in blueprint.items())


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text()

    print(f"Part One: {...}")
    print(f"Part Two: {...}")
