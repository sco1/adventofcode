use day_03;

#[test]
fn test_part_one() {
    assert_eq!(day_03::run_part_one(">"), 2);
    assert_eq!(day_03::run_part_one("^>v<"), 4);
    assert_eq!(day_03::run_part_one("^v^v^v^v^v"), 2);
}

#[test]
fn test_part_two() {
    assert_eq!(day_03::run_part_two("^>"), 3);
    assert_eq!(day_03::run_part_two("^>v<"), 3);
    assert_eq!(day_03::run_part_two("^v^v^v^v^v"), 11);
}
