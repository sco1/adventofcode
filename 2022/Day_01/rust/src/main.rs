use normalize_line_endings::normalized;
use std::fs;
use std::iter::FromIterator;

fn main() {
    let puzzle_input =
        fs::read_to_string(concat!(env!("CARGO_MANIFEST_DIR"), "/../puzzle_input.txt"))
            .expect("Could not open puzzle input.");

    // Normalize newlines between OSes so I can just split on \n\n
    let normalized_inp = &String::from_iter(normalized(puzzle_input.chars()));

    // Calculate the calorie sum of each Elf's snacks
    let mut calorie_counts = normalized_inp
        .split("\n\n") // Elves are delimited by a blank line
        .map(|elf| {
            elf.lines()
                .map(|snack_calories| snack_calories.parse::<u32>().unwrap())
                .sum()
        })
        .collect::<Vec<u32>>();

    // Sort for part 2
    // Can use unstable since we don't care about order of equal elements for this problem
    calorie_counts.sort_unstable();

    println!("Part 1: {}", calorie_counts.last().unwrap());
    println!(
        "Part 2: {}",
        calorie_counts.iter().rev().take(3).sum::<u32>()
    );
}
