use std::fs;

use day_04;

fn main() {
    let secret_key = fs::read_to_string("puzzle_input.txt").expect("Could not open puzzle input.");
    let secret_key = secret_key.trim();

    println!("Part One: {}", day_04::run_part_one(secret_key));
    println!("Part Two: {}", day_04::run_part_two(secret_key));
}
