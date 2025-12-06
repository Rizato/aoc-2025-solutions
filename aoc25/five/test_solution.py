from aoc25.five.solution import DatabaseParser, Inventory


def test_part_one_example():
    parser = DatabaseParser()
    example = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""
    inventory, ids = parser.parse(example)
    assert inventory.get_num_fresh(ids) == 3


def test_part_two_example():
    parser = DatabaseParser()
    example = """3-5
    10-14
    16-20
    12-18

    1
    5
    8
    11
    17
    32"""
    inventory, ids = parser.parse(example)
    assert inventory.get_num_total_inventory() == 14


def test_part_two_double_overlap():
    parser = DatabaseParser()
    example = """3-5
    4-12
    16-20
    12-18
    17-19"""
    inventory, ids = parser.parse(example)
    assert inventory.get_num_total_inventory() == 18


def test_part_two_full_overlap():
    parser = DatabaseParser()
    example = """3-10
    5-7"""
    inventory, ids = parser.parse(example)
    assert inventory.get_num_total_inventory() == 8
