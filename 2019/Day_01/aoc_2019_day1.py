from pathlib import Path


def calculate_propellant(mass: int) -> int:
    """
    Calculate the propellant required to launch a the specified mass.

    To find the fuel required for a specified mass, divide by 3, round down, and subtract 2.
    """
    return (mass // 3) - 2


def calculate_stage_propellant(stage_mass: int) -> int:
    """
    Calculate total propellant required to launch a stage with the specified mass.

    This accounts for launching the propellant rather than just the weight of the dry payload.
    """
    # Account for fuel mass by iterating until the fuel required is <= 0
    total_fuel_mass = 0
    fuel_step = calculate_propellant(stage_mass)
    while fuel_step > 0:
        total_fuel_mass += fuel_step
        fuel_step = calculate_propellant(fuel_step)

    return total_fuel_mass


if __name__ == "__main__":
    puzzle_input = Path("./puzzle_input.txt")

    with puzzle_input.open("r") as f:
        stage_masses = [int(line.strip()) for line in f]

    # Part 1: total fuel required
    print(sum(calculate_propellant(stage) for stage in stage_masses))

    # Part 2: total fuel required, accounting for fuel mass
    print(sum(calculate_stage_propellant(stage) for stage in stage_masses))
