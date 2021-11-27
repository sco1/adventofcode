from textwrap import dedent

import pytest

from .aoc_2020_day13 import find_bus_id, find_golden_timestamp, parse_bus_schedule

SAMPLE_SCHEDULE = dedent(
    """\
    939
    7,13,x,x,59,x,31,19
    """
)


def test_part_one() -> None:  # noqa: D103
    leave_time, bus_ids = parse_bus_schedule(SAMPLE_SCHEDULE)
    bus_id, min_wait_time = find_bus_id(leave_time, bus_ids)

    assert (bus_id * min_wait_time) == 295


PART_TWO_SAMPLES = [
    ("7,13,x,x,59,x,31,19", 1068781),
    ("17,x,13,19", 3417),
    ("67,7,59,61", 754018),
    ("67,x,7,59,61", 779210),
    ("67,7,x,59,61", 1261476),
    ("1789,37,47,1889", 1202161486),
]


@pytest.mark.parametrize(("bus_schedule", "check_timestamp"), PART_TWO_SAMPLES)
def test_part_two(bus_schedule: str, check_timestamp: int) -> None:  # noqa: D103
    assert find_golden_timestamp(bus_schedule) == check_timestamp
