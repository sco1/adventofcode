use std::fs;

use day_03;

fn main() {
    let directions = fs::read_to_string("puzzle_input.txt").expect("Could not open puzzle input.");
    let directions = directions.trim();

    println!("Part One: {}", day_03::run_part_one(directions));
    println!("Part Two: {}", day_03::run_part_two(directions));
}
