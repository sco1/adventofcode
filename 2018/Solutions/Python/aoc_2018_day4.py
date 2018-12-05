import re
from datetime import datetime, timedelta
from itertools import zip_longest
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd


def part1(puzzle_input: List[list]) -> int:
    log_df = build_dataframe(puzzle_input)
    
    sleep_stats = {}
    guard_groupby = log_df.groupby('guard')
    for guard, schedule in guard_groupby:
        minutes_asleep = (schedule.iloc[:,1:] == True).sum().sum()
        sleep_stats[guard] = minutes_asleep

    sleepiest_guard = max(sleep_stats, key=lambda key: sleep_stats[key])
    sleepiest_minute = (guard_groupby.get_group(sleepiest_guard) == True).sum().idxmax()
    
    return sleepiest_guard * sleepiest_minute
    
def build_dataframe(puzzle_input: List[list]) -> pd.DataFrame:
    key_format = r"%Y-%m-%d"
    guard_on_duty = {}  # Keys: date as str, Values: guard ID as int
    sleep_tracker = {}  # Keys: date as str, Values: dict with 'sleep', 'wake' keys, minute values as int
    exp = r"Guard \#(\d+) begins shift"
    for entry in puzzle_input:
        # Keep track of guards on duty for each day
        if entry[1].startswith('Guard'):
            guard_id = int(re.match(exp, entry[1]).groups()[0])
            
            # Check the timestamp for when the guard comes on duty
            tmp_date = entry[0]
            if tmp_date.hour == 23:
                # If they started before midnight, bump them to the next day
                tmp_date += timedelta(hours=1)
                
            guard_on_duty[tmp_date.strftime(key_format)] = guard_id
            continue
        
        date_str = entry[0].strftime(key_format)
        minute = entry[0].minute
        
        if date_str not in sleep_tracker.keys():
            sleep_tracker[date_str] = {}
            
        if entry[1] == "falls asleep":
            if 'sleep' in sleep_tracker[date_str].keys():
                sleep_tracker[date_str]['sleep'].append(minute)
            else:
                sleep_tracker[date_str]['sleep'] = [minute]
        elif entry[1] == "wakes up":
            if 'wake' in sleep_tracker[date_str].keys():
                sleep_tracker[date_str]['wake'].append(minute)
            else:
                sleep_tracker[date_str]['wake'] = [minute]
    else:
        # Sort all sleep/wake times
        for day in sleep_tracker:
            if 'sleep' in sleep_tracker[day]:
                sleep_tracker[day]['sleep'].sort()
            else:
                sleep_tracker[day]['sleep'] = []

            if 'wake' in sleep_tracker[day]:
                sleep_tracker[day]['wake'].sort()
            else:
                sleep_tracker[day]['wake'] = []
    
    # Generate a boolean array for the guards' sleep patterns
    # False: Awake, True: Asleep
    sleep_schedule_list = []
    for day, sleepwake in sleep_tracker.items():
        zipped_sleeps = zip_longest(sleepwake['sleep'], sleepwake['wake'], fillvalue=60)
        day_array = np.zeros(60, dtype=bool)
        for sleep in zipped_sleeps:
              day_array[sleep[0]:sleep[1]] = True
        
        sleep_schedule_list.append(day_array)

    sleep_schedule = np.vstack(sleep_schedule_list)
    
    # Generate DataFrame from sleep_schedule
    sleep_schedule_df = pd.DataFrame(sleep_schedule, index=sleep_tracker.keys())
    # Add column for guard on duty
    guard_series = pd.DataFrame([guard_on_duty[day] for day in sleep_tracker], index=sleep_tracker.keys(), columns=['guard'])
    sleep_schedule_df = pd.concat([guard_series, sleep_schedule_df], axis=1)
    
    return sleep_schedule_df

def part2(puzzle_input: List[list]) -> int:
    raise NotImplementedError

puzzle_input_file = Path("../../Inputs/puzzle_input_d4.txt")
with puzzle_input_file.open(mode="r") as f:
    """
    Parse the input lines

    Group 1: Date (YYYY-MM-DD HH:MM)
    Group 2: Log Entry (full string)
    """
    exp = r"\[([\w\d\s\:\-]+)\]\s+([\w\s\#]+)"
    date_fmt = r"%Y-%m-%d %H:%M"
    puzzle_input = []
    for log_entry in f.readlines():
        match = re.match(exp, log_entry).groups()
        puzzle_input.append([datetime.strptime(match[0], date_fmt), match[1]])

print(part1(puzzle_input))