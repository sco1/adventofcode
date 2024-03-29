from textwrap import dedent

from .aoc_2020_day11 import SeatMap, VisibleSeatMap

SEAT_LAYOUT = dedent(
    """\
    L.LL.LL.LL
    LLLLLLL.LL
    L.L.L..L..
    LLLL.LL.LL
    L.LL.LL.LL
    L.LLLLL.LL
    ..L.L.....
    LLLLLLLLLL
    L.LLLLLL.L
    L.LLLLL.LL
    """
)


def test_seat_stabilization() -> None:
    """Check the number of occupied seats after the Part One boarding process has stabilized."""
    seat_map = SeatMap(SEAT_LAYOUT)
    seat_map.board_until_stable()

    assert seat_map.n_occupied() == 37


def test_visible_seat_stabilization() -> None:
    """Check the number of visible occupied seats after the Part Two boarding process stabilizes."""
    seat_map = VisibleSeatMap(SEAT_LAYOUT, neighbor_threshold=5)
    seat_map.board_until_stable()

    assert seat_map.n_occupied() == 26
