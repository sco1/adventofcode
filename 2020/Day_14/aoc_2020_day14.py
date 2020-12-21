import itertools as it
import re
from pathlib import Path


class FerryComputer:  # noqa: D101
    MASK_RE = re.compile(r"mask = (\w+)")  # Captures entire bit mask string
    ASSIGN_RE = re.compile(r"mem\[(\d+)\] = (\d+)")  # Captures address & value

    memory_register: dict[int, int]

    bitmask: str
    _andmask: int
    _ormask: int

    def __init__(self, initialization_program: str, is_v2: bool = False) -> None:
        self.initialization_program = initialization_program
        self.is_v2 = is_v2

        self.memory_register = {}

    @property
    def initialization_value(self) -> int:
        """Calculate the sum of all the values currently in memory."""
        return sum(self.memory_register.values())

    def set_mask(self, mask: str) -> None:
        """
        Store the bitmask & cache the appropriate transforms based on decoder version.

        Integer AND and OR masks are generated & cached for downstream use. The general application
        of the masks is of the form `new_value = value & AND_MASK | OR_MASK`.

        If `self.is_v2` is `False`, then the `X` values of the bitmask are transformed into masks
        such that the `X` values do not modify the incoming value

        Otherwise, the masks are set such that `0` does not modify the incoming value, `1`
        overwrites the bit with `1`, and `X` is replaced with `0`. "Floating" values are handled
        explicitly by the register access method.
        """
        self.bitmask = mask

        self._ormask = int(self.bitmask.replace("X", "0"), 2)
        if not self.is_v2:
            self._andmask = int(self.bitmask.replace("X", "1"), 2)
        else:
            self._andmask = int(self.bitmask.replace("0", "1").replace("X", "0"), 2)

    def access_registers(self, address: int, value: int) -> None:
        """
        Assign value to memory address(es) based on the decoder chip version.

        If `self.is_v2` is `False`, then the memory address is utilized as-is and the mask is
        applied to the value.

        Otherwise, the mask is used as a memory address decoder:
            * If the mask bit is `0`, the corresponding memory address bit is unchanged
            * If the mask bit is `1`, the corresponding memory address bit is overwritten with `1`
            * If the mask bit is `X`, the corresponding memory address bit is floating

        Floating bits will take on all possible values, which may cause multiple memory addresses to
        be written to. For the version 2 decoder the value is passed as-is.
        """
        if not self.is_v2:
            self.memory_register[address] = value & self._andmask | self._ormask
            return

        # If we're using the v2 decoder, map out all of the combinations of floating bits
        #
        # Rewind backwards through the bitmask to find the bit locations from least -> most
        # significant bits, since we'll be using these locations as powers of 2
        powers = [x_idx for x_idx, char in enumerate(self.bitmask[::-1]) if char == "X"]
        for flip_bits in it.product((0, 1), repeat=len(powers)):  # Generate bit combinations
            address = address & self._andmask | self._ormask
            for power, bit in zip(powers, flip_bits):
                if bit:  # Since our AND mask replaces X with 0, we can skip these
                    address |= 2 ** power  # Use bitwise or to flip the appropriate bit

            self.memory_register[address] = value

    def run_program(self) -> None:
        """Run through the loaded initialization code."""
        for line in self.initialization_program.splitlines():
            if mask_check := self.MASK_RE.findall(line):
                self.set_mask(mask_check[0])
                continue

            address, value = [int(val) for val in self.ASSIGN_RE.findall(line)[0]]
            self.access_registers(address, value)


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text()

    computer = FerryComputer(puzzle_input)
    computer.run_program()
    print(f"Part One: {computer.initialization_value}")

    computer = FerryComputer(puzzle_input, is_v2=True)
    computer.run_program()
    print(f"Part Two: {computer.initialization_value}")
