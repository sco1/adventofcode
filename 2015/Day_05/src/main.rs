use std::fs;

use day_05;

fn main() {
    let word_list = fs::read_to_string("puzzle_input.txt").expect("Could not open puzzle input.");
    let word_list = word_list.trim();

    println!("Part One: {}", day_05::run_part_one(word_list));
    println!("Part Two: {}", day_05::run_part_two(word_list));
}
