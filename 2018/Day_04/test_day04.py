from textwrap import dedent

from .aoc_2018_day4 import (
    _build_sleep_schedule,
    _parse_logs,
    find_sleepiest_guard,
    find_sleepiest_minute,
)

SAMPLE_LOGS = dedent(
    """\
    [1518-11-01 00:00] Guard #10 begins shift
    [1518-11-01 00:05] falls asleep
    [1518-11-01 00:25] wakes up
    [1518-11-01 00:30] falls asleep
    [1518-11-01 00:55] wakes up
    [1518-11-01 23:58] Guard #99 begins shift
    [1518-11-02 00:40] falls asleep
    [1518-11-02 00:50] wakes up
    [1518-11-03 00:05] Guard #10 begins shift
    [1518-11-03 00:24] falls asleep
    [1518-11-03 00:29] wakes up
    [1518-11-04 00:02] Guard #99 begins shift
    [1518-11-04 00:36] falls asleep
    [1518-11-04 00:46] wakes up
    [1518-11-05 00:03] Guard #99 begins shift
    [1518-11-05 00:45] falls asleep
    [1518-11-05 00:55] wakes up
    """
).splitlines()
LOGS = _parse_logs(SAMPLE_LOGS)
SCHEDULE = _build_sleep_schedule(LOGS)


def test_part_one() -> None:
    guard_id, minutes_asleep = find_sleepiest_guard(SCHEDULE)
    assert (guard_id * minutes_asleep) == 240


def test_part_two() -> None:
    guard_id, sleepiest_minute = find_sleepiest_minute(SCHEDULE)
    assert (guard_id * sleepiest_minute) == 4455
