from pathlib import Path


class Sleigh:
    """Basic helper class to model Santa's movement & present delivery."""

    def __init__(self):
        """Initialize the sleigh object & deliver a present to the first household."""
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
        """Move the sleigh one grid left."""
        self.x -= 1

    def move_right(self):
        """Move the sleigh one grid right."""
        self.x += 1

    def move_up(self):
        """Move the sleigh one grid up."""
        self.y += 1

    def move_down(self):
        """Move the sleigh one grid down."""
        self.y -= 1

    def make_moves(self, move_list: str):
        """Make present deliveries based on the input `move_list`."""
        for move in move_list:
            self.movement_mapping[move]()
            try:
                self.presents_delivered[(self.x, self.y)] += 1
            except KeyError:
                self.presents_delivered[(self.x, self.y)] = 1

    def at_least_one(self) -> int:
        """Return the number of households with at least one present."""
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

# Use a set intersection to remove duplicate households
print(
    len(
        set(santas_sleigh.presents_delivered.keys())
        | set(robot_santas_sleigh.presents_delivered.keys())
    )
)
