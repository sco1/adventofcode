use std::fs;

fn main() {
    let secret_key =
        fs::read_to_string(concat!(env!("CARGO_MANIFEST_DIR"), "/../puzzle_input.txt"))
            .expect("Could not open puzzle input.");
    let secret_key = secret_key.trim();

    println!("Part One: {}", y2015_d04::run_part_one(secret_key));
    println!("Part Two: {}", y2015_d04::run_part_two(secret_key));
}
