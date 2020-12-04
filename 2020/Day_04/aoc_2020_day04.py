from __future__ import annotations

import re
import typing as t
from dataclasses import dataclass, fields
from functools import partial
from pathlib import Path


@dataclass
class Passport:
    """Represents your North Pole Passport!"""

    byr: t.Optional[int] = None  # Birth Year
    iyr: t.Optional[int] = None  # Issue Year
    eyr: t.Optional[int] = None  # Expiration Year
    hgt: t.Optional[str] = None  # Height (<measurement><unit>, e.g. "183cm")
    hcl: t.Optional[str] = None  # Hair Color (hex)
    ecl: t.Optional[str] = None  # Eye Color
    pid: t.Optional[str] = None  # Passport ID (can have leading zeros)
    cid: t.Optional[int] = None  # Country ID

    _int_fields = set(("byr", "iyr", "eyr", "cid"))  # Convert these to int while parsing

    def __post_init__(self):
        self._available_fields = frozenset(field.name for field in fields(self))

        self._validators = {
            "byr": partial(self.year_validator, start_year=1920, end_year=2002),
            "iyr": partial(self.year_validator, start_year=2010, end_year=2020),
            "eyr": partial(self.year_validator, start_year=2020, end_year=2030),
            "hgt": self.height_validator,
            "hcl": self.hair_color_validator,
            "ecl": self.eye_color_validator,
            "pid": self.passport_id_validator,
            "cid": lambda _: True,  # No validation
        }

    def is_valid(self, optional_fields: tuple[str], validate_data: bool = False) -> bool:
        """
        Check validity of the current passport instance.

        A passport is considered valid if all fields not marked as optional are present.
        """
        fields_to_check = self._available_fields - set(optional_fields)

        presence_check = all(getattr(self, field) is not None for field in fields_to_check)
        if not presence_check:
            return False

        if validate_data:
            data_valid_check = all(
                self._validators[field](getattr(self, field)) for field in fields_to_check
            )
            return data_valid_check

        # If we've gotten here the passport should be valid.
        return True

    @classmethod
    def from_raw_string(cls, raw_string: str) -> Passport:
        """Parse the provided raw batch passport string into a `Passport` instance."""
        parsed_kv = {}
        for kv_pair in raw_string.split():
            key, value = kv_pair.split(":")
            if key in cls._int_fields:
                value = int(value)

            parsed_kv[key] = value

        return cls(**parsed_kv)

    @staticmethod
    def year_validator(query_date: int, start_year: int, end_year: int) -> bool:
        """Check that the provided year falls within the provided start & end dates, inclusive."""
        return start_year <= query_date <= end_year

    @staticmethod
    def height_validator(query_value: str) -> bool:
        """
        Check that the height field is specified properly.

        Heights are assumed to be formatted as <measurement><unit>, where:
            * Unit must be `"cm"` or `"in"`
                * If centimeters, must be between [150, 193]
                * If inches, must be between [59, 96]
        """
        pattern = r"(\d+)(in|cm)"
        match_check = re.findall(pattern, query_value)

        if not match_check:
            return False

        measurement, unit = match_check[0]
        if unit == "in":
            return 59 <= int(measurement) <= 76
        elif unit == "cm":
            return 150 <= int(measurement) <= 193

    @staticmethod
    def hair_color_validator(query_value: str) -> bool:
        """
        Check that the hair color field is specified properly.

        Valid hair colors must be a `#` followed by exactly six characters `0-9` or `a-f`
        """
        pattern = r"#[0-9a-f]{6}$"
        return re.match(pattern, query_value)

    @staticmethod
    def eye_color_validator(query_value: str) -> bool:
        """
        Check that the eye color field is specified properly.

        Eye colors must be exactly one of: "amb", "blu", "brn", "gry", "grn", "hzl", or "oth"
        """
        valid_colors = set(("amb", "blu", "brn", "gry", "grn", "hzl", "oth"))
        return query_value in valid_colors

    @staticmethod
    def passport_id_validator(query_value: str) -> bool:
        """
        Check that the passport ID field is specified properly.

        Passport IDs must be a nine-digit number, and may include leading zeros
        """
        return len(query_value) == 9 and query_value.isdigit()


def parse_batch_file(batch_file: str) -> list[Passport]:
    """
    Parse the provided batch processing file into a collection of `Passport` instances.

    The batch file is assumed to contain one or more passports represented as a sequence of
    key:value pairs delimited by spaces and/or newlines. Individual passports are separated by a
    blank line.
    """
    passports = []
    # Split on blank lines to get individual passports
    for line in batch_file.split("\n\n"):
        # Concatenate passport lines into one string for simpler parsing
        passports.append(Passport.from_raw_string(line.replace("\n", " ")))

    return passports


def check_passports(
    passports: list[Passport], optional_fields: tuple[str], validate_data: bool = False
) -> int:
    """
    Count the number of valid Passports in the provided list.

    A passport is considered valid if all fields not marked as optional are present.
    """
    return sum(passport.is_valid(optional_fields, validate_data) for passport in passports)


if __name__ == "__main__":
    puzzle_input_file = Path("./puzzle_input.txt")
    puzzle_input = puzzle_input_file.read_text()

    passports = parse_batch_file(puzzle_input)
    print(f"Part One: {check_passports(passports, ('cid',))} valid passports")
    print(f"Part Two: {check_passports(passports, ('cid',), True)} valid passports")
