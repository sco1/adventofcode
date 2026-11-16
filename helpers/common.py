from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
FIRST_EVENT_YEAR = 2015


def puzzle_dir(year: int, day: int, base_dir: Path = BASE_DIR) -> Path:
    """Return the folder for the given year & day's puzzle, e.g. `<base_dir>/2015/Day_01`."""
    return base_dir / f"{year}" / f"Day_{day:02d}"


def n_puzzle_days(year: int) -> int:
    """Return the number of puzzle days in the given event year."""
    # Starting in 2025, the event is 12 days long rather than the historical 25
    if year >= 2025:
        return 12
    else:
        return 25


def validate_puzzle_date(year: int, day: int) -> None:
    """Raise `ValueError` if the given year & day do not correspond to an event puzzle."""
    if year < FIRST_EVENT_YEAR:
        raise ValueError(f"year must be {FIRST_EVENT_YEAR} or later (got {year})")

    n_days = n_puzzle_days(year)
    if not 1 <= day <= n_days:
        raise ValueError(f"day must be between 1 and {n_days} for {year} (got {day})")
