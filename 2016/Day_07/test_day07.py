import pytest

from .aoc_2016_day07 import supports_ssl, supports_tls

TLS_TEST_CASES = (
    ("abba[mnop]qrst", True),
    ("abcd[bddb]xyyx", False),
    ("aaaa[qwer]tyui", False),
    ("ioxxoj[asdfgh]zxcvbn", True),
    ("ioxxoj[asdfgh]zxcvbn[bddb]xyyx", False),
)


@pytest.mark.parametrize(("address", "truth_supports"), TLS_TEST_CASES)
def test_supports_tls(address: str, truth_supports: bool) -> None:
    assert supports_tls(address) is truth_supports


SSL_TEST_CASES = (
    ("aba[bab]xyz", True),
    ("xyx[xyx]xyx", False),
    ("aaa[kek]eke", True),
    ("zazbz[bzb]cdb", True),
)


@pytest.mark.parametrize(("address", "truth_supports"), SSL_TEST_CASES)
def test_supports_ssl(address: str, truth_supports: bool) -> None:
    assert supports_ssl(address) is truth_supports
