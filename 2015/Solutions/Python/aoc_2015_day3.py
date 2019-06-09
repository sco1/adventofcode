from pathlib import Path


class Sleigh:
    def __init__(self):
        self.x = 0
        self.y = 0

        self.movement_mapping = {
            "<": self.move_left,
            ">": self.move_right,
            "^": self.move_up,
            "v": self.move_down,
        }

        self.presents_delivered = {(self.x, self.y): 1}

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

    def move_up(self):
        self.y += 1

    def move_down(self):
        self.y -= 1

    def make_moves(self, move_list: str):
        for move in move_list:
            self.movement_mapping[move]()
            try:
                self.presents_delivered[(self.x, self.y)] += 1
            except KeyError:
                self.presents_delivered[(self.x, self.y)] = 1

    def at_least_one(self) -> int:
        return len(self.presents_delivered)


puzzle_input_file = Path("../../Inputs/puzzle_input_d3.txt")
with puzzle_input_file.open(mode="r") as f:
    puzzle_input = f.read()

# Part 1
santas_sleigh = Sleigh()
santas_sleigh.make_moves(puzzle_input)
print(santas_sleigh.at_least_one())

# Part 2
santas_sleigh = Sleigh()
robot_santas_sleigh = Sleigh()
santas_sleigh.make_moves(puzzle_input[::2])
robot_santas_sleigh.make_moves(puzzle_input[1::2])
print(
    len(
        set(santas_sleigh.presents_delivered.keys())
        | set(robot_santas_sleigh.presents_delivered.keys())
    )
)
