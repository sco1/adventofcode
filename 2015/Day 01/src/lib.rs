/// Help Santa navigate the large apartment building!
///
/// `puzzle_input` is a string of parentheses, where `(` goes up one floor and `)` goes down one floor
///
/// Returns the destination floor.
pub fn part_one(puzzle_input: &str) -> i32 {
    let mut floor = 0;
    for c in puzzle_input.chars() {
        match c {
            '(' => floor += 1,
            ')' => floor -= 1,
            _ => panic!("Unknown instruction encountered"),
        }
    }

    floor
}

/// Find where Santa enters the basement!
///
/// `puzzle_input` is a string of parentheses, where `(` goes up one floor and `)` goes down one floor
///
/// Returns the step index where Santa first enters the basement (`floor = -1`)
pub fn part_two(puzzle_input: &str) -> Result<usize, &str> {
    let mut floor = 0;
    for (idx, c) in puzzle_input.chars().enumerate() {
        match c {
            '(' => floor += 1,
            ')' => floor -= 1,
            _ => panic!("Unknown instruction encountered"),
        }

        if floor == -1 {
            return Ok(idx + 1); // indices are zero-indexed so we need to add 1 to get the step #
        }
    }

    Err("Basement could not be reached")
}
