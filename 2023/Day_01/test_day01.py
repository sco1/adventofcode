import pytest

from .aoc_2023_day01 import extract_calibration_value

EXTRACTION_CASES = (
    ("1abc2", 12),
    ("pqr3stu8vwx", 38),
    ("a1b2c3d4e5f", 15),
    ("treb7uchet", 77),
)


@pytest.mark.parametrize(("calibration_string", "truth_value"), EXTRACTION_CASES)
def test_calibration_extraction(calibration_string: str, truth_value: int) -> None:
    assert extract_calibration_value(calibration_string) == truth_value


EXTRACTION_CASES_WITH_WORDS = (
    ("two1nine", 29),
    ("eightwothree", 83),
    ("abcone2threexyz", 13),
    ("xtwone3four", 24),
    ("4nineeightseven2", 42),
    ("zoneight234", 14),
    ("7pqrstsixteen", 76),
    ("269hzeightwoz", 22),
)


@pytest.mark.parametrize(("calibration_string", "truth_value"), EXTRACTION_CASES_WITH_WORDS)
def test_calibration_extraction_advanced(calibration_string: str, truth_value: int) -> None:
    assert extract_calibration_value(calibration_string, include_spelled=True) == truth_value
