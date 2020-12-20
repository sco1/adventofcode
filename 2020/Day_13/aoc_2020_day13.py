from pathlib import Path

from sympy.ntheory.modular import crt


def parse_bus_schedule(raw_schedule: str) -> tuple[int, list[int]]:
    """
    Parse the provided bus schedule into its components.

    The provided schedule is assumed to be of the following form:
        939
        7,13,x,x,59,x,31,19

    Where the first line is the earliest timestamp we can depart and the second line lists the IDs
    of the busses currently in service. "x" entries are ignored.
    """
    leave_time, bus_ids = raw_schedule.splitlines()

    leave_time = int(leave_time)
    bus_ids = [int(bus_id) for bus_id in bus_ids.split(",") if bus_id != "x"]

    return leave_time, bus_ids


def find_bus_id(leave_time: int, bus_ids: list[int]) -> tuple[int, int]:
    """
    Find the ID and wait time for the bus departing soonest after our earliest leave time.

    Busses are assumed to leave at timestamp 0 and then at every multiple of their ID afterwards.

    NOTE: Per the problem statement, it is assumed that there is exactly one bus that meets our
    criteria.
    """
    # Find the next bus by looking at the time mod for our earliest leave time
    # The delta of this mod and the bus IDs will give us the wait time for the next bus departure
    delta_nearest = (leave_time % bus_id for bus_id in bus_ids)

    # Since we need the bus ID and the delta, use wait time, bus ID key,value pairs for lookup
    wait_times = {(bus_id - nearest): bus_id for nearest, bus_id in zip(delta_nearest, bus_ids)}

    min_wait_time = min(wait_times.keys())
    bus_id = wait_times[min_wait_time]

    return bus_id, min_wait_time


def find_golden_timestamp(bus_schedule: str) -> int:
    """
    Find the earliest timestamp where bus departures flow according to their schedule position.

    For example, given the schedule `"7,x,2,11"` we want to find the earliest timestamp, `t`, where
    Bus 7 departs at `t`, Bus 2 departs at `t+2`, and Bus 11 departs at `t+3`.

    NOTE: For simplification purposes, Bus IDs are assumed to be prime
    """
    parsed_schedule = [
        (int(bus_id), -1 * offset)  # Negate offset so CRT will calculate appropriately
        for offset, bus_id in enumerate(bus_schedule.split(","))
        if bus_id != "x"
    ]

    # I used these links to help try and get an understanding of what is happening with the maths:
    #    https://eli.thegreenplace.net/2019/the-chinese-remainder-theorem/
    #    https://en.wikipedia.org/wiki/Modular_multiplicative_inverse
    bus_ids = [slot[0] for slot in parsed_schedule]
    offsets = [slot[1] for slot in parsed_schedule]
    return crt(bus_ids, offsets, check=False)[0]


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text()

    leave_time, bus_ids = parse_bus_schedule(puzzle_input)
    bus_id, min_wait_time = find_bus_id(leave_time, bus_ids)
    print(f"Part One: {bus_id * min_wait_time}")

    print(f"Part Two: t={find_golden_timestamp(puzzle_input.splitlines()[1])}")
