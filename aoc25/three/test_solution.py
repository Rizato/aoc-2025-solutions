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
