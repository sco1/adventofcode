from textwrap import dedent

from .aoc_2021_day10 import parse_subsystem_code, score_autocomplete

SAMPLE_INPUT = dedent(
    """\
    [({(<(())[]>[[{[]{<()<>>
    [(()[<>])]({[<{<<[]>>(
    {([(<{}[<>[]}>{[]{[(<()>
    (((({<>}<{<{<>}{[]{[]{}
    [[<[([]))<([[{}[[()]]]
    [{[{({}]{}}([{[{{{}}([]
    {<[[]]>}<{[{[{[]{()[[[]
    [<(<(<(<{}))><([]([]()
    <{([([[(<>()){}]>(<<{{
    <{([{{}}[<[[[<>{}]]]>[]]
    """
).splitlines()


def test_part_one() -> None:
    syntax_score, _ = parse_subsystem_code(SAMPLE_INPUT)
    assert syntax_score == 26397


def test_part_two() -> None:
    _, incomplete_lines = parse_subsystem_code(SAMPLE_INPUT)
    assert score_autocomplete(incomplete_lines) == 288957
