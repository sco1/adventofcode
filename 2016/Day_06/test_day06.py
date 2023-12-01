from textwrap import dedent

from .aoc_2022_day06 import correct_message

SAMPLE_INPUT = dedent(
    """\
    eedadn
    drvtee
    eandsr
    raavrd
    atevrs
    tsrnev
    sdttsa
    rasrtv
    nssdts
    ntnada
    svetve
    tesnvt
    vntsnd
    vrdear
    dvrsen
    enarar
    """
)


def test_error_correction() -> None:
    assert correct_message(SAMPLE_INPUT) == "easter"
    assert correct_message(SAMPLE_INPUT, most_common=False) == "advent"
