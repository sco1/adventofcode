import datetime as dt
import re
import typing as t
from collections import defaultdict, deque
from enum import Enum, auto
from operator import itemgetter
from pathlib import Path

LOG_RE = re.compile(r"\[([\w\s\:\-]+)\] ([\w\s\#]+)")
SHIFT_RE = re.compile(r"Guard #(\d+)")

DT_FMT = r"%Y-%m-%d %H:%M"

SLEEP_SCHEDULE = dict[int, dict[int, int]]


class LogType(Enum):  # noqa: D101
    SLEEP = auto()
    WAKE = auto()
    SHIFT = auto()


class LogEntry(t.NamedTuple):  # noqa: D101
    timestamp: dt.datetime
    log_type: LogType
    guard_id: int


def _parse_logs(log_entries: list[str]) -> list[LogEntry]:
    """
    Parse the provided log entries into a chronological feed.

    Entries are assumed to be one of the following types:
        * `[<timestamp>] Guard #<id> begins shift`
        * `[<timestamp>] falls asleep`
        * `[<timestamp>] wakes up`

    NOTE: The guard sleeping/waking is assumed to be the one whose shift most recently started.
    NOTE: All asleep/awake times are assumed to be during the midnight hour.
    NOTE: Input log entries are not guaranteed to be in chronologal order
    """
    # In order to correctly associate log entries with their guard, we need to parse the timestamps
    # first so we can sort chronologically
    semi_parsed = []
    for log in log_entries:
        raw_timestamp, raw_entry = LOG_RE.findall(log)[0]
        timestamp = dt.datetime.strptime(raw_timestamp, DT_FMT)
        semi_parsed.append((timestamp, raw_entry))

    chronological = sorted(semi_parsed, key=itemgetter(0))

    # Now we have a chronological feed & can associate events with their respective guard on duty
    on_duty = -1
    parsed_schedule = []
    for timestamp, raw_entry in chronological:
        # Check for shift change first so we can update the guard on duty
        if shift_change := SHIFT_RE.findall(raw_entry):
            on_duty = int(shift_change[0])
            parsed_schedule.append(LogEntry(timestamp, LogType.SHIFT, on_duty))
            continue

        match raw_entry:
            case "falls asleep":
                parsed_schedule.append(LogEntry(timestamp, LogType.SLEEP, on_duty))
            case "wakes up":
                parsed_schedule.append(LogEntry(timestamp, LogType.WAKE, on_duty))
            case _:
                raise ValueError(f"Unknown log entry at {timestamp}, '{raw_entry}'")

    return parsed_schedule


def _build_sleep_schedule(logs: list[LogEntry]) -> SLEEP_SCHEDULE:
    """
    Generate a sleep schedule for the guard(s) on duty from the provided log entries.

    For each guard, a dictionary is built whose keys are the minute(s) they're found asleep and
    whose values are a count of the number of times they're encountered asleep at that minute.

    NOTE: Per the problem statement, it's assumed that all asleep/awake times are between `00:00`
    and `00:59`, so only the minute portion of the timestamp is considered for this schedule.
    """
    sleep_schedule: SLEEP_SCHEDULE = defaultdict(lambda: defaultdict(int))
    log_queue = deque(logs)

    sleep_time = wake_time = None
    while log_queue:
        entry = log_queue.popleft()
        if entry.log_type == LogType.SHIFT:
            # Don't care about shift changes any more
            continue

        if entry.log_type == LogType.SLEEP:
            sleep_time = entry.timestamp
            continue

        # Once the guard wakes up we can increment their time spent sleeping
        if entry.log_type == LogType.WAKE:
            wake_time = entry.timestamp
            for minute in range(sleep_time.minute, wake_time.minute):
                sleep_schedule[entry.guard_id][minute] += 1

            sleep_time = wake_time = None

    return sleep_schedule


def find_sleepiest_guard(schedule: SLEEP_SCHEDULE) -> tuple[int, int]:
    """Identify the sleepiest guard and the minute they're asleep the most."""
    time_asleep = []
    for guard in schedule:
        asleep = sum(schedule[guard].values())
        time_asleep.append((guard, asleep))

    time_asleep.sort(key=itemgetter(1))
    sleepiest_guard = time_asleep[-1][0]
    sleepiest_minute = max(schedule[sleepiest_guard], key=schedule[sleepiest_guard].get)

    return sleepiest_guard, sleepiest_minute


def find_sleepiest_minute(schedule: SLEEP_SCHEDULE) -> tuple[int, int]:
    """Identify the guard most frequently asleep on the same minute, along with the minute."""
    max_minutes = []
    for guard in schedule:
        sleepiest_minute = max(schedule[guard], key=schedule[guard].get)
        max_minutes.append((guard, sleepiest_minute, schedule[guard][sleepiest_minute]))

    max_minutes.sort(key=itemgetter(2))
    sleepiest_guard, sleepiest_minute, _ = max_minutes[-1]

    return sleepiest_guard, sleepiest_minute


if __name__ == "__main__":
    puzzle_input_file = Path("puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text().splitlines()

    logs = _parse_logs(puzzle_input)
    schedule = _build_sleep_schedule(logs)

    guard_id, minutes_asleep = find_sleepiest_guard(schedule)
    print(f"Part One: {guard_id * minutes_asleep}")

    guard_id, sleepiest_minute = find_sleepiest_minute(schedule)
    print(f"Part Two: {guard_id * sleepiest_minute}")
