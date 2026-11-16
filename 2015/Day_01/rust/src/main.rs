use std::fs;

fn main() {
    let directions =
        fs::read_to_string(concat!(env!("CARGO_MANIFEST_DIR"), "/../puzzle_input.txt"))
            .expect("Could not open puzzle input.");
    let directions = directions.trim();

    println!("Part One: Floor {}", y2015_d01::part_one(&directions));
    println!(
        "Part Two: Step {}",
        y2015_d01::part_two(&directions).unwrap()
    );
}
