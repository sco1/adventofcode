use day_01;

#[test]
fn test_part_one() {
    assert_eq!(day_01::part_one("(())"), 0);
    assert_eq!(day_01::part_one("()()"), 0);
    assert_eq!(day_01::part_one("((("), 3);
    assert_eq!(day_01::part_one("(()(()("), 3);
    assert_eq!(day_01::part_one("))((((("), 3);
    assert_eq!(day_01::part_one("())"), -1);
    assert_eq!(day_01::part_one("))("), -1);
    assert_eq!(day_01::part_one(")))"), -3);
    assert_eq!(day_01::part_one(")())())"), -3);
}

#[test]
fn test_part_two() {
    assert_eq!(day_01::part_two(")").unwrap(), 1);
    assert_eq!(day_01::part_two("()())").unwrap(), 5);
}
