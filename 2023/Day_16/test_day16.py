from .aoc_2023_day16 import find_max_energized, fire_beam, parse_cavern_map

SAMPLE_INPUT = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""

CAVERN_MAP, CAVERN_BBOX = parse_cavern_map(SAMPLE_INPUT)


def test_energized_tiles() -> None:
    assert len(fire_beam(CAVERN_MAP, CAVERN_BBOX)) == 46


def test_max_energized() -> None:
    assert find_max_energized(CAVERN_MAP, CAVERN_BBOX) == 51
