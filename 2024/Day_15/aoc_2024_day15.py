from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from pathlib import Path

from helpers.geometry import BoundingBox, COORD, MoveDir
from helpers.parsing import parse_map_objects


def parse_warehouse_map(raw_map: str) -> tuple[set[COORD], set[COORD], COORD]:
    """
    Parse the provided warehouse map into its components.

    The warehouse map is assumed to be provided as a grid of characters, where `#` represents a
    wall, `O` represents a box, and `@` represents the robot worker's start location.
    """
    walls = set()
    boxes = set()
    start_loc: COORD | None = None

    for loc, c in parse_map_objects(raw_map):
        match c:
            case "#":
                walls.add(loc)
            case "O":
                boxes.add(loc)
            case "@":
                start_loc = loc
            case _:
                raise ValueError(f"Unexpected character encountered at {loc}: '{c}'")

    if start_loc is None:
        raise ValueError("Could not locate robot's starting location")

    return walls, boxes, start_loc


def parse_instructions(raw_instructions: str) -> list[MoveDir]:
    """
    Parse the provided instructions into their components.

    Instructions are assumed to be provided as a string of `<`, `^`, `>`, and `v` characters,
    representing cardinal movement directions. Any newline characters, if present, are ignored.
    """
    # Newlines within move sequence are ignored
    raw_instructions = "".join(raw_instructions.splitlines())

    instructions = []
    for c in raw_instructions:
        match c:
            case "<":
                instructions.append(MoveDir.WEST)
            case "^":
                instructions.append(MoveDir.NORTH)
            case ">":
                instructions.append(MoveDir.EAST)
            case "v":
                instructions.append(MoveDir.SOUTH)
            case _:
                raise ValueError(f"Unexpected character encountered: '{c}'")

    return instructions


@dataclass(slots=True)
class Warehouse:  # noqa: D101
    walls: set[COORD]
    boxes: set[COORD]
    robot_loc: COORD
    instructions: list[MoveDir]

    _bbox: BoundingBox = field(init=False)

    def __post_init__(self) -> None:
        # Build the warehouse's bounding box, assuming that the walls fully enclose the area
        self._bbox = BoundingBox(self.walls)

    def render(self) -> str:  # noqa: D102
        rows = []
        for y in self._bbox.y_bound:
            cols = []
            for x in self._bbox.x_bound:
                if (x, y) in self.walls:
                    cols.append("#")
                elif (x, y) in self.boxes:
                    cols.append("O")
                elif (x, y) == self.robot_loc:
                    cols.append("@")
                else:
                    cols.append(".")

            rows.append("".join(cols))

        return "\n".join(rows)

    def execute_instructions(self) -> None:
        """
        Have the robot worker execute its provided instructions.

        For each instruction, the robot attempts to move in the specified direction:
            * If the target location is an empty space, the robot moves into that space
            * If the target location is a wall, the robot does not move
            * If the target location contains a box, the robot will attempt to push the box
                * If the space beyond the target box is a wall, neither the robot nor the box moves
                * If the space beyond the target box is empty, the box is pushed into that space by
                the robot, and the robot moves into the space vacated
                * If the space beyond the target box is one or more boxes, the robot will attempt to
                push the stack: If there is an empty space at the end of the stack, the boxes will
                all shift and the robot moves into the space vacated, otherwise if there is a wall
                then neither the robot nor the box stack moves
        """
        ins_queue = deque(self.instructions)
        while ins_queue:
            move = ins_queue.popleft()
            target = move.shift(self.robot_loc)

            if target in self.walls:
                # Bonked into a wall
                continue
            elif target in self.boxes:
                # Robot has encountered a box, first see what is along the path
                boxes_can_move = [target]
                box_target = move.shift(target)
                while True:
                    if box_target in self.walls:
                        # The box(es) are against a wall and cannot move, nor can the robot
                        boxes_can_move.clear()
                        break
                    elif box_target in self.boxes:
                        # The stack of boxes grows
                        boxes_can_move.append(box_target)
                        box_target = move.shift(box_target)
                    else:
                        # A free space for the box(es) has been found
                        break

                if boxes_can_move:
                    # If the boxes are able to move, shift all of them along the move direction and
                    # put the robot into the vacated space
                    while boxes_can_move:
                        box = boxes_can_move.pop()
                        self.boxes.remove(box)
                        self.boxes.add(move.shift(box))

                    self.robot_loc = target
            else:
                # Empty space
                self.robot_loc = target

    def calculate_gps_score(self) -> int:
        """
        Calculate the total GPS score for the warehouse's box locations.

        The GPS score of each box is calculated as `100` times its distance from the top edge of the
        map plus its distance from the left edge of the map. Note that the exterior wall tiles are
        included in this calculation.

        For example, the following box has a GPS score of `100 * 1 + 4 = 104`:

        ```
        #######
        #...O..
        #......
        ```
        """
        gps_score = 0
        for box in self.boxes:
            x, y = box
            gps_score += 100 * y + x

        return gps_score

    @classmethod
    def from_raw(cls, raw_document: str) -> Warehouse:
        """
        Build a `Warehouse` instance from the provided documentation.

        Documentation is assumed to be provided as the warehouse map, then a blank line, then the
        robot worker's instructions, e.g.:

        ```
        ########
        #..O.O.#
        ##@.O..#
        #...O..#
        #.#.O..#
        #...O..#
        #......#
        ########

        <^^>>>vv<v>>v<<
        ```

        See the documentation for `parse_warehouse_map` and `parse_instructions` for assumptions on
        their respective forms.
        """
        raw_map, raw_instructions = raw_document.split("\n\n")
        walls, boxes, start_loc = parse_warehouse_map(raw_map)
        instructions = parse_instructions(raw_instructions)

        return cls(
            walls=walls,
            boxes=boxes,
            robot_loc=start_loc,
            instructions=instructions,
        )


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().strip()

    warehouse = Warehouse.from_raw(puzzle_input)
    warehouse.execute_instructions()

    print(f"Part One: {warehouse.calculate_gps_score()}")
    print(f"Part Two: {...}")
