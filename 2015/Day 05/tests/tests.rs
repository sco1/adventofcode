use day_05;

#[test]
fn test_part_one() {
    assert_eq!(day_05::run_part_one("ugknbfddgicrmopn"), 1);
    assert_eq!(day_05::run_part_one("aaa"), 1);
    assert_eq!(day_05::run_part_one("jchzalrnumimnmhp"), 0);
    assert_eq!(day_05::run_part_one("haegwjzuvuyypxyu"), 0);
    assert_eq!(day_05::run_part_one("dvszwmarrgswjxmb"), 0);
}

#[test]
fn test_part_two() {
    assert_eq!(day_05::run_part_two("qjhvhtzxzqqjkmpb"), 1);
    assert_eq!(day_05::run_part_two("xxyxx"), 1);
    assert_eq!(day_05::run_part_two("uurcxstgmygtbstg"), 0);
    assert_eq!(day_05::run_part_two("ieodomkazucvgmuy"), 0);
}
