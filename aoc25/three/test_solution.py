from aoc25.three.solution import BatteryBank, JoltageCalculator


def test_part_one_examples():
    assert (
        JoltageCalculator.find_max_joltage_part_one(
            BatteryBank.parse_bank("987654321111111")
        )
        == 98
    )
    assert (
        JoltageCalculator.find_max_joltage_part_one(
            BatteryBank.parse_bank("811111111111119")
        )
        == 89
    )
    assert (
        JoltageCalculator.find_max_joltage_part_one(
            BatteryBank.parse_bank("234234234234278")
        )
        == 78
    )
    assert (
        JoltageCalculator.find_max_joltage_part_one(
            BatteryBank.parse_bank("818181911112111")
        )
        == 92
    )


def test_part_two_examples():
    assert (
        JoltageCalculator.find_max_joltage_part_two_bf(
            BatteryBank.parse_bank("987654321111111"), 12
        )
        == 987654321111
    )
    assert (
        JoltageCalculator.find_max_joltage_part_two_bf(
            BatteryBank.parse_bank("811111111111119"), 12
        )
        == 811111111119
    )
    assert (
        JoltageCalculator.find_max_joltage_part_two_bf(
            BatteryBank.parse_bank("234234234234278"), 12
        )
        == 434234234278
    )
    assert (
        JoltageCalculator.find_max_joltage_part_two_bf(
            BatteryBank.parse_bank("818181911112111"), 12
        )
        == 888911112111
    )


def test_part_two_last_11_max():
    assert (
        JoltageCalculator.find_max_joltage_part_two_bf(
            BatteryBank.parse_bank("1111199999999999"), 12
        )
        == 199999999999
    )


def test_part_two_largest_last():
    assert (
        JoltageCalculator.find_max_joltage_part_two_bf(
            BatteryBank.parse_bank("1234567123456789"), 12
        )
        == 567123456789
    )


def test_part_two_largest_first():
    assert (
        JoltageCalculator.find_max_joltage_part_two_bf(
            BatteryBank.parse_bank("9111111111111111"), 12
        )
        == 911111111111
    )


def test_part_two_examples_linear():
    assert (
        JoltageCalculator.find_max_joltage_part_two_linear(
            BatteryBank.parse_bank("987654321111111"), 12
        )
        == 987654321111
    )
    assert (
        JoltageCalculator.find_max_joltage_part_two_linear(
            BatteryBank.parse_bank("811111111111119"), 12
        )
        == 811111111119
    )
    assert (
        JoltageCalculator.find_max_joltage_part_two_linear(
            BatteryBank.parse_bank("234234234234278"), 12
        )
        == 434234234278
    )
    assert (
        JoltageCalculator.find_max_joltage_part_two_linear(
            BatteryBank.parse_bank("818181911112111"), 12
        )
        == 888911112111
    )


def test_part_two_last_11_max_linear():
    assert (
        JoltageCalculator.find_max_joltage_part_two_linear(
            BatteryBank.parse_bank("1111199999999999"), 12
        )
        == 199999999999
    )


def test_part_two_largest_last_linear():
    assert (
        JoltageCalculator.find_max_joltage_part_two_linear(
            BatteryBank.parse_bank("1234567123456789"), 12
        )
        == 567123456789
    )


def test_part_two_largest_first_linear():
    assert (
        JoltageCalculator.find_max_joltage_part_two_linear(
            BatteryBank.parse_bank("9111111111111111"), 12
        )
        == 911111111111
    )


def test_part_two_cycling_linear():
    assert (
        JoltageCalculator.find_max_joltage_part_two_linear(
            BatteryBank.parse_bank("123456789098765432123456789"), 12
        )
        == 998765456789
    )


def test_part_two_multi_larger():
    assert (
        JoltageCalculator.find_max_joltage_part_two_linear(
            BatteryBank.parse_bank("1123456789098765432123456789"), 12
        )
        == 998765456789
    )
