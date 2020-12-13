from textwrap import dedent

from .aoc_2020_day13 import find_bus_id, parse_bus_schedule


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
