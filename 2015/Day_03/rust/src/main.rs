use std::fs;

fn main() {
    let directions =
        fs::read_to_string(concat!(env!("CARGO_MANIFEST_DIR"), "/../puzzle_input.txt"))
            .expect("Could not open puzzle input.");
    let directions = directions.trim();

    println!("Part One: {}", y2015_d03::run_part_one(directions));
    println!("Part Two: {}", y2015_d03::run_part_two(directions));
}
