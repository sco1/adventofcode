from textwrap import dedent

import pytest

from .aoc_2024_day14 import Robot, RobotGrid

SAMPLE_ROBOTS = dedent(
    """\
    p=0,4 v=3,-3
    p=6,3 v=-1,-3
    p=10,3 v=-1,2
    """
)
TRUTH_ROBOTS = [
    Robot(position=(0, 4), velocity=(3, -3)),
    Robot(position=(6, 3), velocity=(-1, -3)),
    Robot(position=(10, 3), velocity=(-1, 2)),
]


def test_robot_parse() -> None:
    parsed_bots = [Robot.from_raw(ln) for ln in SAMPLE_ROBOTS.splitlines()]
    assert parsed_bots == TRUTH_ROBOTS


SAMPLE_GRID_ROBOTS = dedent(
    """\
    p=0,4 v=3,-3
    p=6,3 v=-1,-3
    p=10,3 v=-1,2
    p=2,0 v=2,-1
    p=0,0 v=1,3
    p=3,0 v=-2,-2
    p=7,6 v=-1,-3
    p=3,0 v=-1,-2
    p=9,3 v=2,3
    p=7,3 v=-1,2
    p=2,4 v=2,-3
    p=9,5 v=-3,-3
    """
)

TRUTH_RENDERED = dedent(
    """\
    1.12.......
    ...........
    ...........
    ......11.11
    1.1........
    .........1.
    .......1..."""
)


def test_grid_render() -> None:
    parsed_bots = [Robot.from_raw(ln) for ln in SAMPLE_GRID_ROBOTS.splitlines()]
    grid = RobotGrid(width=11, height=7, robots=parsed_bots)

    assert grid.render_grid() == TRUTH_RENDERED


STEP_CASES = (
    (
        dedent(
            """\
            ...........
            ...........
            ...........
            ...........
            ..1........
            ...........
            ..........."""
        ),
        0,
    ),
    (
        dedent(
            """\
            ...........
            ....1......
            ...........
            ...........
            ...........
            ...........
            ..........."""
        ),
        1,
    ),
    (
        dedent(
            """\
            ...........
            ...........
            ...........
            ...........
            ...........
            ......1....
            ..........."""
        ),
        2,
    ),
    (
        dedent(
            """\
            ...........
            ...........
            ........1..
            ...........
            ...........
            ...........
            ..........."""
        ),
        3,
    ),
    (
        dedent(
            """\
            ...........
            ...........
            ...........
            ...........
            ...........
            ...........
            ..........1"""
        ),
        4,
    ),
    (
        dedent(
            """\
            ...........
            ...........
            ...........
            .1.........
            ...........
            ...........
            ..........."""
        ),
        5,
    ),
)


@pytest.mark.parametrize(("truth_rendered, n_steps"), STEP_CASES)
def test_step_sim(truth_rendered: str, n_steps: int) -> None:
    robot = Robot.from_raw("p=2,4 v=2,-3")
    grid = RobotGrid(width=11, height=7, robots=[robot])

    grid.step(n_steps)
    assert grid.render_grid() == truth_rendered


def test_full_sim() -> None:
    parsed_bots = [Robot.from_raw(ln) for ln in SAMPLE_GRID_ROBOTS.splitlines()]
    grid = RobotGrid(width=11, height=7, robots=parsed_bots)

    TRUTH_SIM_RENDERED = dedent(
        """\
        ......2..1.
        ...........
        1..........
        .11........
        .....1.....
        ...12......
        .1....1...."""
    )

    grid.step(100)
    assert grid.render_grid() == TRUTH_SIM_RENDERED


def test_calculate_safety_factor() -> None:
    parsed_bots = [Robot.from_raw(ln) for ln in SAMPLE_GRID_ROBOTS.splitlines()]
    grid = RobotGrid(width=11, height=7, robots=parsed_bots)

    grid.step(100)
    assert grid.calculate_safety_factor() == 12
