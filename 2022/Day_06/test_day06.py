import pytest

from .aoc_2022_day06 import locate_start_marker

SAMPLE_BUFFERS_PACKET = (
    ("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 7),
    ("bvwbjplbgvbhsrlpgdmjqwftvncz", 5),
    ("nppdvjthqldpwncqszvftbrmjlhg", 6),
    ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 10),
    ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 11),
)


@pytest.mark.parametrize(("data_buffer", "start_marker"), SAMPLE_BUFFERS_PACKET)
def test_find_packet_start(data_buffer: str, start_marker: int) -> None:
    assert locate_start_marker(data_buffer, 4) == start_marker


SAMPLE_BUFFERS_MESSAGE = (
    ("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 19),
    ("bvwbjplbgvbhsrlpgdmjqwftvncz", 23),
    ("nppdvjthqldpwncqszvftbrmjlhg", 23),
    ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 29),
    ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 26),
)


@pytest.mark.parametrize(("data_buffer", "start_marker"), SAMPLE_BUFFERS_MESSAGE)
def test_find_message_start(data_buffer: str, start_marker: int) -> None:
    assert locate_start_marker(data_buffer, 14) == start_marker
