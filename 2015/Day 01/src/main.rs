use std::fs;

use day_01;

fn main() {
    let directions = fs::read_to_string("puzzle_input.txt").expect("Could not open puzzle input.");
    let directions = directions.trim();

    println!("Part One: Floor {}", day_01::part_one(&directions));
    println!("Part Two: Step {}", day_01::part_two(&directions).unwrap());
}
