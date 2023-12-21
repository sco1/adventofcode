from textwrap import dedent

import pytest

from .aoc_2023_day20 import parse_module_configuration, press_button

SAMPLE_INPUT_1 = dedent(
    """\
    broadcaster -> a, b, c
    %a -> b
    %b -> c
    %c -> inv
    &inv -> a
    """
)

SAMPLE_INPUT_2 = dedent(
    """\
    broadcaster -> a
    %a -> inv, con
    &inv -> b
    %b -> con
    &con -> output
    """
)

BUTTON_PRESS_TEST_CASES = (
    (SAMPLE_INPUT_1, 32, 32_000_000),
    (SAMPLE_INPUT_2, 16, 11_687_500),
)


@pytest.mark.parametrize(
    ("module_map", "truth_1_press", "truth_1000_press"), BUTTON_PRESS_TEST_CASES
)
def test_button_press(module_map: str, truth_1_press: int, truth_1000_press: int) -> None:
    modules = parse_module_configuration(module_map)
    assert press_button(modules, n_presses=1) == truth_1_press
    assert press_button(modules, n_presses=1000) == truth_1000_press
