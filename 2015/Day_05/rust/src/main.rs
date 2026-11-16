use std::fs;

fn main() {
    let word_list = fs::read_to_string(concat!(env!("CARGO_MANIFEST_DIR"), "/../puzzle_input.txt"))
        .expect("Could not open puzzle input.");
    let word_list = word_list.trim();

    println!("Part One: {}", y2015_d05::run_part_one(word_list));
    println!("Part Two: {}", y2015_d05::run_part_two(word_list));
}
