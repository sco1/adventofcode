from pathlib import Path

from IntcodeComputer import IntcodeMachine


if __name__ == "__main__":
    puzzle_input = Path("./puzzle_input.txt")

    with puzzle_input.open("r") as f:
        in_program = [int(code) for code in f.read().strip().split(",")]

    # Part 1
    computer = IntcodeMachine(in_program, stdin="1")
    computer.run()
    print(computer.stdout)

    # Part 2
    computer = IntcodeMachine(in_program, stdin="5")
    computer.run()
    print(computer.stdout)
