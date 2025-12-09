from aoc25.nine.solution import RedTileParser


def test_part_one_example():
    parser = RedTileParser()
    example = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""
    red_tiles = parser.parse(example)

    assert red_tiles.find_largest_area() == 50


def test_part_two_example():
    parser = RedTileParser()
    example = """7,1
    11,1
    11,7
    9,7
    9,5
    2,5
    2,3
    7,3"""
    red_tiles = parser.parse(example)

    assert red_tiles.find_largest_area_part_two() == 24


def test_part_two_overlapping():
    parser = RedTileParser()
    example = """7,1
    11,1
    11,7
    9,7
    9,5
    2,5
    2,3
    7,3
    5,5"""  # 5, 5 is in line with the pivot, but makes a smaller area than 9, 5
    red_tiles = parser.parse(example)

    assert red_tiles.find_largest_area_part_two() == 24
