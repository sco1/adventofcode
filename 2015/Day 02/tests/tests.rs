use day_02;

#[test]
fn test_part_one() {
    assert_eq!(day_02::find_total_wrapping("2x3x4"), 58);
    assert_eq!(day_02::find_total_wrapping("1x1x10"), 43);
}

#[test]
fn test_part_two() {
    assert_eq!(day_02::find_total_ribbon("2x3x4"), 34);
    assert_eq!(day_02::find_total_ribbon("1x1x10"), 14);
}
