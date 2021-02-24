use std::fs;

use day_02;

fn main() {
    let present_dimensions =
        fs::read_to_string("puzzle_input.txt").expect("Could not open puzzle input.");
    let present_dimensions = present_dimensions.trim();

    println!(
        "Part One: {} square feet",
        day_02::find_total_wrapping(present_dimensions)
    );
    println!(
        "Part Two: {} feet",
        day_02::find_total_ribbon(present_dimensions)
    );
}
