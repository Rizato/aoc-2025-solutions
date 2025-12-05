from aoc25.five.solution import FreshCounter


def test_part_one_example():
    counter = FreshCounter()
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
    assert counter.count_fresh(example) == 3


def test_part_two_example():
    counter = FreshCounter()
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
    assert counter.count_fresh(example) == 3
