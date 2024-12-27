from textwrap import dedent

import pytest

from .aoc_2024_day24 import Wiring, parse_schematic, run_circuit, wire_and, wire_or, wire_xor

SAMPLE_INPUT = dedent(
    """\
    x00: 1
    x01: 1
    x02: 1
    y00: 0
    y01: 1
    y02: 0

    x00 AND y00 -> z00
    x01 XOR y01 -> z01
    x02 OR y02 -> z02
    """
)

LONGER_SAMPLE_INPUT = dedent(
    """\
    x00: 1
    x01: 0
    x02: 1
    x03: 1
    x04: 0
    y00: 1
    y01: 1
    y02: 1
    y03: 1
    y04: 1

    ntg XOR fgs -> mjb
    y02 OR x01 -> tnw
    kwq OR kpj -> z05
    x00 OR x03 -> fst
    tgd XOR rvg -> z01
    vdt OR tnw -> bfw
    bfw AND frj -> z10
    ffh OR nrd -> bqk
    y00 AND y03 -> djm
    y03 OR y00 -> psh
    bqk OR frj -> z08
    tnw OR fst -> frj
    gnj AND tgd -> z11
    bfw XOR mjb -> z00
    x03 OR x00 -> vdt
    gnj AND wpb -> z02
    x04 AND y00 -> kjc
    djm OR pbm -> qhw
    nrd AND vdt -> hwm
    kjc AND fst -> rvg
    y04 OR y02 -> fgs
    y01 AND x02 -> pbm
    ntg OR kjc -> kwq
    psh XOR fgs -> tgd
    qhw XOR tgd -> z09
    pbm OR djm -> kpj
    x03 XOR y03 -> ffh
    x00 XOR y04 -> ntg
    bfw OR bqk -> z06
    nrd XOR fgs -> wpb
    frj XOR qhw -> z04
    bqk OR frj -> z07
    y03 OR x01 -> nrd
    hwm AND bqk -> z03
    tgd XOR rvg -> z12
    tnw OR pbm -> gnj
    """
)

TRUTH_INITIAL_STATE = {
    "x00": 1,
    "x01": 1,
    "x02": 1,
    "y00": 0,
    "y01": 1,
    "y02": 0,
}
TRUTH_WIRING = [
    Wiring(left="x00", op=wire_and, right="y00", target="z00"),
    Wiring(left="x01", op=wire_xor, right="y01", target="z01"),
    Wiring(left="x02", op=wire_or, right="y02", target="z02"),
]


def test_parse_schematic() -> None:
    initial_values, wiring = parse_schematic(SAMPLE_INPUT)
    assert initial_values == TRUTH_INITIAL_STATE
    assert wiring == TRUTH_WIRING


CIRCUIT_TEST_CASES = ((SAMPLE_INPUT, 4), (LONGER_SAMPLE_INPUT, 2024))


@pytest.mark.parametrize(("schematic", "truth_val"), CIRCUIT_TEST_CASES)
def test_circuit(schematic: str, truth_val: int) -> None:
    assert run_circuit(*parse_schematic(schematic)) == truth_val
