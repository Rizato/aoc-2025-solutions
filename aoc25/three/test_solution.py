from aoc25.three.solution import BatteryBank, JoltageCalculator


def test_part_one_examples():
    assert 98 == JoltageCalculator.find_max_joltage(
        BatteryBank.parse_bank("987654321111111")
    )
    assert 89 == JoltageCalculator.find_max_joltage(
        BatteryBank.parse_bank("811111111111119")
    )
    assert 78 == JoltageCalculator.find_max_joltage(
        BatteryBank.parse_bank("234234234234278")
    )
    assert 92 == JoltageCalculator.find_max_joltage(
        BatteryBank.parse_bank("818181911112111")
    )


def test_part_two_examples():
    assert 987654321111 == JoltageCalculator.find_max_joltage_part_two_dp(
        BatteryBank.parse_bank("987654321111111"), 12
    )
    assert 811111111119 == JoltageCalculator.find_max_joltage_part_two_dp(
        BatteryBank.parse_bank("811111111111119"), 12
    )
    assert 434234234278 == JoltageCalculator.find_max_joltage_part_two_dp(
        BatteryBank.parse_bank("234234234234278"), 12
    )
    assert 888911112111 == JoltageCalculator.find_max_joltage_part_two_dp(
        BatteryBank.parse_bank("818181911112111"), 12
    )


def test_part_two_last_11_max():
    assert 199999999999 == JoltageCalculator.find_max_joltage_part_two_dp(
        BatteryBank.parse_bank("1111199999999999"), 12
    )


def test_part_two_largest_last():
    assert 567123456789 == JoltageCalculator.find_max_joltage_part_two_dp(
        BatteryBank.parse_bank("1234567123456789"), 12
    )


def test_part_two_largest_first():
    assert 911111111111 == JoltageCalculator.find_max_joltage_part_two_dp(
        BatteryBank.parse_bank("9111111111111111"), 12
    )
