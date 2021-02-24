use std::collections::HashSet;

fn visit(step: char, x: &mut i32, y: &mut i32, visited: &mut HashSet<(i32, i32)>) {
    match step {
        '^' => *y += 1,
        '>' => *x += 1,
        'v' => *y -= 1,
        '<' => *x -= 1,
        _ => panic!("Unknown step instruction"),
    };
    visited.insert((*x, *y));
}

pub fn run_part_one(directions: &str) -> usize {
    let mut visited = HashSet::new();
    visited.insert((0, 0)); // Begin by delivering to the house at the starting location

    let (mut x, mut y) = (0, 0);

    for step in directions.chars() {
        visit(step, &mut x, &mut y, &mut visited);
    }

    visited.len()
}

pub fn run_part_two(directions: &str) -> usize {
    let mut visited = HashSet::new();
    visited.insert((0, 0)); // Begin by delivering to the house at the starting location

    let (mut x_santa, mut y_santa) = (0, 0);
    let (mut x_robot, mut y_robot) = (0, 0);

    // Real Santa & Robot Santa take turns following the steps, starting with Real Santa
    // So Real Santa will be consuming the even steps & Robot Santa the odds
    for (idx, step) in directions.char_indices() {
        if idx % 2 == 0 {
            visit(step, &mut x_santa, &mut y_santa, &mut visited);
        } else {
            visit(step, &mut x_robot, &mut y_robot, &mut visited);
        }
    }

    visited.len()
}
