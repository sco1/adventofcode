from __future__ import annotations

from pathlib import Path

from intcode.machine import IntcodeMachine, find_noun_verb

# Tests for this day are contained in ./intcode/test_machine.py

if __name__ == "__main__":
    puzzle_input = Path("./puzzle_input.txt")
    in_program = puzzle_input.read_text().strip()

    # Part 1
    im = IntcodeMachine(in_program)
    im.run(noun=12, verb=2)
    print(im.output)

    # Part 2
    noun, verb = find_noun_verb(in_program, 19690720)
    print(100 * noun + verb)
