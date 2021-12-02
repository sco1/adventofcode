from collections import namedtuple
from pathlib import Path

Command = namedtuple("command", ["instruction", "magnitude"])


class SubMcSubFace:
    """The Advent of Code Submarine!"""

    aim: int
    depth: int
    horizontal: int

    parsed_commands: list[Command]

    def __init__(self, raw_commands: list[str], is_aiming: bool = False) -> None:
        self._raw_commands = raw_commands
        self.is_aiming = is_aiming

        self.parse_commands()
        self.reset()

    def parse_commands(self) -> None:
        """
        Process the raw commands into a set of `Command` instructions.

        Raw commands are assumed to be of the form `<instruction> <magnitude>`, and the following
        instructions are supported:
            * `"forward"`
            * `"down"`
            * `"up"`

        Magnitudes are assumed to be integers.
        """
        self.parsed_commands = []
        for line in self._raw_commands:
            instruction, magnitude = line.strip().split(" ")
            self.parsed_commands.append(Command(instruction, int(magnitude)))

    def reset(self) -> None:
        """Reset the sub to its initial state."""
        self.aim = 0
        self.depth = 0
        self.horizontal = 0

    def _step_basic(self, command: Command) -> None:
        """
        Interpret command instructions per the YOLO submarine manual-less instructions.

        Instructions are interpreted as written.
        """
        match command.instruction:
            case "forward":
                self.horizontal += command.magnitude
            case "down":
                self.depth += command.magnitude
            case "up":
                self.depth -= command.magnitude
            case _:
                raise ValueError(f"Unknown instruction '{command.instruction}'")

    def _step_aiming(self, command: Command) -> None:
        """
        Interpret command instructions per the more complicated submarine manual.

        The `"up"` and `"down"` change the submarine's `aim`, and the `"forward"` instruction
        modifies both the horizontal position and depth of the submarine.
        """
        match command.instruction:
            case "forward":
                self.horizontal += command.magnitude
                self.depth += command.magnitude * self.aim
            case "down":
                self.aim += command.magnitude
            case "up":
                self.aim -= command.magnitude
            case _:
                raise ValueError(f"Unknown instruction '{command.instruction}'")

    def run(self) -> None:
        """
        Execute the parsed commands & send our sub into glory.

        Command interpretation is controlled by the instance's `is_aiming` flag.
        """
        if self.is_aiming:
            for command in self.parsed_commands:
                self._step_aiming(command)
        else:
            for command in self.parsed_commands:
                self._step_basic(command)


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().splitlines()

    toot_toot = SubMcSubFace(puzzle_input)
    toot_toot.run()
    print(f"Part One: {toot_toot.horizontal * toot_toot.depth}")

    toot_toot.reset()
    toot_toot.is_aiming = True
    toot_toot.run()
    print(f"Part Two: {toot_toot.horizontal * toot_toot.depth}")
