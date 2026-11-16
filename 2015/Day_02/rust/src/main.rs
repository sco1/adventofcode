use std::fs;

fn main() {
    let present_dimensions =
        fs::read_to_string(concat!(env!("CARGO_MANIFEST_DIR"), "/../puzzle_input.txt"))
            .expect("Could not open puzzle input.");
    let present_dimensions = present_dimensions.trim();

    println!(
        "Part One: {} square feet",
        y2015_d02::find_total_wrapping(present_dimensions)
    );
    println!(
        "Part Two: {} feet",
        y2015_d02::find_total_ribbon(present_dimensions)
    );
}
