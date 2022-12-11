import typing as t
from pathlib import Path


def execute_program(instructions: t.Iterable[str]) -> t.Iterable[tuple[int, int]]:
    """
    Execute the provided instructions & yield the current cycle & register values.

    The CPU has a single register, which starts with the value `1`. It supports only two
    instructions:
        * `addx V` takes two cycles to complete. After two cycles, the register is increased by the
        value `V`. (`V` can be negative.)
        * `noop` takes one cycle to complete. It has no other effect.
    """
    cycle = 1
    register = 1
    for instruction in instructions:
        if instruction.startswith("noop"):
            yield (cycle, register)
            cycle += 1
            continue

        _, n = instruction.split()
        val = int(n)
        for _ in range(2):
            yield (cycle, register)
            cycle += 1
        else:
            register += val


def debug_register(instructions: t.Iterable[str], query_cycles: t.Iterable[int]) -> t.Iterable[int]:
    """
    Execute the provided instructions & yield the signal strength at the queried cycle(s).

    The signal strength is calculated as the product of the currently ending cycle and the register
    value.

    The CPU has a single register, which starts with the value `1`. It supports only two
    instructions:
        * `addx V` takes two cycles to complete. After two cycles, the register is increased by the
        value `V`. (`V` can be negative.)
        * `noop` takes one cycle to complete. It has no other effect.
    """
    for cycle, register_val in execute_program(instructions):
        if cycle in query_cycles:
            yield cycle * register_val


def render_image(
    instructions: t.Iterable[str], screen_size: tuple[int, int] = (40, 6), sprite_size: int = 3
) -> str:
    """
    Execute the provided instructions & return the resulting image produced by the CRT.

    The register controls the horizontal position of the middle of a sprite. The CRT draws a single
    pixel during each CPU cycle; if the sprite is positioned such that one of its pixels is the
    pixel currently being drawn, the screen produces a lit pixel, otherwise the screen leaves the
    pixel dark.

    This CRT is assumed to draw the pixels in each row from left to right, then move on to the next
    row on the screen. As a result, the sprite's position only has a horizontal component.
    """
    width, _ = screen_size
    half_sprite = sprite_size // 2

    pixel_rows: list[str] = []
    row_buffer: list[str] = []
    for cycle, register_val in execute_program(instructions):
        col = (cycle - 1) % width
        if row_buffer and col == 0:
            pixel_rows.append("".join(row_buffer))
            row_buffer.clear()

        # Leave the sprite indices as 1-based since we're also assuming the register gives a 1-based
        # sprite midpoint position
        sprite_idx = range(
            max(register_val - half_sprite, 0),
            min(register_val + half_sprite + 1, width),
        )
        if col in sprite_idx:
            row_buffer.append("#")
        else:
            row_buffer.append(".")

    # Make sure we dump the last row
    if row_buffer:
        pixel_rows.append("".join(row_buffer))

    return "\n".join(pixel_rows)


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().splitlines()

    QUERY_CYCLES = (20, 60, 100, 140, 180, 220)
    print(f"Part One: {sum(debug_register(puzzle_input, QUERY_CYCLES))}")
    print(f"Part Two:\n{render_image(puzzle_input)}")
