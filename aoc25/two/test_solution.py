from aoc25.two.solution import ProductRange


def test_find_valid_number_part_two():
    assert ProductRange.is_id_valid_part_two(10121011)


def test_find_invalid_number_part_two():
    assert not ProductRange.is_id_valid_part_two(10121012)
    assert not ProductRange.is_id_valid(10121012)


def test_find_invalid_number_trio():
    assert not ProductRange.is_id_valid_part_two(101210121012)


def test_find_invalid_number_quat():
    assert not ProductRange.is_id_valid_part_two(10121012101210121012)


def test_find_valid_number_many_repeats():
    assert ProductRange.is_id_valid_part_two(1111111111112)


def test_find_valid_number_by_cut_off():
    assert ProductRange.is_id_valid_part_two(1011101)


def test_find_valid_number_by_cut_off_again():
    assert ProductRange.is_id_valid_part_two(1012101)


def test_starting_number_repeats_at_midpoint():
    assert not ProductRange.is_id_valid_part_two(292292)


def test_starting_number_repeats_at_boundary():
    assert not ProductRange.is_id_valid_part_two(292292292)


def test_examples():
    assert not ProductRange.is_id_valid_part_two(11)
    assert not ProductRange.is_id_valid_part_two(22)
    assert not ProductRange.is_id_valid_part_two(99)
    assert not ProductRange.is_id_valid_part_two(1010)
    assert not ProductRange.is_id_valid_part_two(1188511885)
    assert not ProductRange.is_id_valid_part_two(222222)
    assert not ProductRange.is_id_valid_part_two(446446)
    assert not ProductRange.is_id_valid_part_two(38593859)
    assert not ProductRange.is_id_valid_part_two(565656)
    assert not ProductRange.is_id_valid_part_two(824824824)
    assert not ProductRange.is_id_valid_part_two(2121212121)
