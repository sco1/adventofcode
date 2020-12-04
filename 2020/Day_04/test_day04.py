import typing as t
from textwrap import dedent

import pytest

from .aoc_2020_day04 import check_passports, parse_batch_file


class PassportTestCase(t.NamedTuple):
    """Helper container for optional field validation test cases."""

    optional_fields: tuple[str]
    n_valid_passports: int


PT1_BATCH = dedent(
    """\
    ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
    byr:1937 iyr:2017 cid:147 hgt:183cm

    iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
    hcl:#cfa07d byr:1929

    hcl:#ae17e1 iyr:2013
    eyr:2024
    ecl:brn pid:760753108 byr:1931
    hgt:179cm

    hcl:#cfa07d eyr:2025 pid:166559648
    iyr:2011 ecl:brn hgt:59in
    """
)

PASSPORT_TEST_CASES = [
    PassportTestCase(("cid",), 2),
]


@pytest.mark.parametrize(("optional_fields", "n_valid_passports"), PASSPORT_TEST_CASES)
def test_passport_validation_pt1(optional_fields: tuple[str], n_valid_passports: int) -> None:
    """
    Test automated batch passport validation with the specified ignored data fields.

    This does not check validation of individual field values.
    """
    passports = parse_batch_file(PT1_BATCH)

    assert check_passports(passports, optional_fields) == n_valid_passports


PT2_INVALID = dedent(
    """\
    eyr:1972 cid:100
    hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

    iyr:2019
    hcl:#602927 eyr:1967 hgt:170cm
    ecl:grn pid:012533040 byr:1946

    hcl:dab227 iyr:2012
    ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

    hgt:59cm ecl:zzz
    eyr:2038 hcl:74454a iyr:2023
    pid:3556412378 byr:2007
    """
)

PT2_VALID = dedent(
    """\
    pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
    hcl:#623a2f

    eyr:2029 ecl:blu cid:129 byr:1989
    iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

    hcl:#888785
    hgt:164cm byr:2001 iyr:2015 cid:88
    pid:545766238 ecl:hzl
    eyr:2022

    iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
    """
)


def test_passport_validation_pt2() -> None:
    """Check the provided valid and invalid passports for correct data validation."""
    invalid_passports = parse_batch_file(PT2_INVALID)
    assert check_passports(invalid_passports, ("cid",), True) == 0

    valid_passports = parse_batch_file(PT2_VALID)
    assert check_passports(valid_passports, ("cid",), True) == 4
