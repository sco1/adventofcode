from pathlib import Path

from intcode.machine import IntcodeMachine

if __name__ == "__main__":
    puzzle_input = Path("./puzzle_input.txt")
    in_program = puzzle_input.read_text().strip()

    # Part 1
    computer = IntcodeMachine(in_program, stdin="1")
    computer.run()
    print(computer.stdout[0])

    # Part 2
    computer = IntcodeMachine(in_program, stdin="5")
    computer.run()
    print(computer.stdout[0])
