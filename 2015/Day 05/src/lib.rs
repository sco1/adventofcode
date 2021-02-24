use counter::Counter;
use itertools::Itertools;

const VOWELS: [char; 5] = ['a', 'e', 'i', 'o', 'u'];
const NAUGHTY_SUBSTR: [&str; 4] = ["ab", "cd", "pq", "xy"];

fn vowel_counter(in_str: &str) -> u32 {
    let mut vowel_count = 0;

    for c in in_str.chars() {
        if VOWELS.contains(&c) {
            vowel_count += 1;
        }
    }

    vowel_count
}

fn has_consecutive_duplicate(in_str: &str) -> bool {
    for (_, group) in &in_str.chars().group_by(|c| *c) {
        let group: Vec<char> = group.collect();
        if group.len() > 1 {
            return true;
        }
    }

    false
}

fn has_naughty_substring(in_str: &str) -> bool {
    for &substr in NAUGHTY_SUBSTR.iter() {
        if in_str.contains(&substr) {
            return true;
        }
    }

    false
}

/// Check if a word is nice according to the rules for Part One.
fn is_nice_a(word: &str) -> bool {
    // Check vowel count
    if vowel_counter(&word) < 3 {
        return false;
    }

    // Check for at least 1 pair of consecutive duplicate characters
    if !has_consecutive_duplicate(&word) {
        return false;
    }

    // Check for forbidden substrings
    if has_naughty_substring(&word) {
        return false;
    }

    true
}

fn has_repeat_nonoverlapping_pair(word: &str) -> bool {
    let chunk_counts = &word.as_bytes().windows(2).collect::<Counter<_>>();
    for (_, freq) in chunk_counts.most_common() {
        if freq > 1 {
            return true;
        }
    }

    false
}

fn has_bookended_triple(word: &str) -> bool {
    for window in word.as_bytes().windows(3) {
        let window = String::from_utf8_lossy(window);
        if window.chars().nth(0) == window.chars().nth(2) {
            return true;
        }
    }

    false
}

/// Check if a word is nice according to the rules for Part Two.
fn is_nice_b(word: &str) -> bool {
    // Check for duplicate, nonoverlapping pairs
    if !has_repeat_nonoverlapping_pair(&word) {
        return false;
    }

    if !has_bookended_triple(&word) {
        return false;
    }

    true
}

/// Count the number of nice words in the provided newline delimited word list.
///
/// A nice word is determined by the following criteria:
///   * Contains at least 3 vowels (aeiou)
///   * Contains at least one letter that appears twice in a row
///   * Does not contain the strings 'ab', 'cd', 'pq', or 'xy'
pub fn run_part_one(word_list: &str) -> usize {
    word_list.lines().filter(|line| is_nice_a(line)).count()
}

/// Count the number of nice words in the provided newline delimited word list.
///
/// A nice word is determined by the following criteria:
///   * Contains a pair of any two letters that appear at least twice without overlapping
///   * Contains at least one letter which repeats with exactly one letter between
pub fn run_part_two(word_list: &str) -> usize {
    word_list.lines().filter(|line| is_nice_b(line)).count()
}
