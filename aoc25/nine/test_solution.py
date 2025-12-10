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
    print(red_tiles.draw_floor())
    assert red_tiles.find_largest_area_part_two() == 24


def test_part_two_example_reordered():
    parser = RedTileParser()
    example = """9,7
    9,5
    2,5
    2,3
    7,3
    7,1
    11,1
    11,7"""
    red_tiles = parser.parse(example)
    print(red_tiles.draw_floor())
    assert red_tiles.find_largest_area_part_two() == 24


def test_part_two_example_reordered_slight_change():
    parser = RedTileParser()
    example = """8,7
    8,5
    2,5
    2,3
    7,3
    7,1
    11,1
    11,7"""
    red_tiles = parser.parse(example)
    print(red_tiles.draw_floor())
    assert red_tiles.find_largest_area_part_two() == 28


def test_part_two_double_back():
    #  abbbbbbbbbba
    #  bbabbbbbbabb
    #  bbb      bbb
    #  aba      aba
    parser = RedTileParser()
    example = """0,0
    11,0
    11,3
    9,3
    9,1
    2,1
    2,3
    0,3"""
    red_tiles = parser.parse(example)
    print(red_tiles.draw_floor())
    assert red_tiles.find_largest_area_part_two() == 20


def test_part_two_double_back_wider_taller():
    #  abbbbbbbbbbbba
    #  bbbbbbbbbbbbbb
    #  bbbabbbbbbabbb
    #  bbbb      bbbb
    #  abba      abba
    parser = RedTileParser()
    example = """0,0
    13,0
    13,4
    10,4
    10,2
    3,2
    3,4
    0,4"""
    red_tiles = parser.parse(example)
    print(red_tiles.draw_floor())
    assert red_tiles.find_largest_area_part_two() == 33


def test_part_two_top_hole():
    #  abba      abba
    #  bbbb      bbbb
    #  bbbabbbbbbabbb
    #  abbbbbbbbbbbba
    parser = RedTileParser()
    example = """0,0
    3,0
    3,2
    10,2
    10,0
    13,0
    13,3
    0,3"""
    red_tiles = parser.parse(example)
    print(red_tiles.draw_floor())
    assert red_tiles.find_largest_area_part_two() == 22


def test_part_two_left_hole():
    #  abbbba
    #  bbbbbb
    #  ababbb
    #    bbbb
    #    bbbb
    #  ababba
    #  bbbbbb
    #  abbbba
    parser = RedTileParser()
    example = """0,0
        5,0
        5,7
        0,7
        0,5
        2,5
        2,2
        0,2"""
    red_tiles = parser.parse(example)
    print(red_tiles.draw_floor())
    assert red_tiles.find_largest_area_part_two() == 24


def test_part_two_right_hole():
    #  abbbba
    #  bbbbbb
    #  bbbaba
    #  bbbb
    #  bbbb
    #  bbbaba
    #  bbbbbb
    #  abbbba
    parser = RedTileParser()
    example = """0,0
    5,0
    5,2
    3,2
    3,5
    5,5
    5,7
    0,7"""
    red_tiles = parser.parse(example)
    print(red_tiles.draw_floor())
    assert red_tiles.find_largest_area_part_two() == 24


def test_part_two_double_back_surround():
    #  abbbbbbbbbba
    #  bbabbbbbbabb
    #  bbb      bbb
    #  aba      bbb
    #           bbb
    #     abbbbbabb
    #     bbbbbbbbb
    #     abbbbbbba
    parser = RedTileParser()
    example = """0,0
    11,0
    11,7
    3,7
    3,5
    9,5
    9,1
    2,1
    2,3
    0,3"""
    red_tiles = parser.parse(example)
    print(red_tiles.draw_floor())
    assert red_tiles.find_largest_area_part_two() == 27


def test_part_two_line():
    parser = RedTileParser()
    example = """9,7
    9,5
    9,8
    9,9
    9,10
    9,12
    9,3
    9,4
    9,1"""
    red_tiles = parser.parse(example)
    print(red_tiles.draw_floor())
    assert red_tiles.find_largest_area_part_two() == 12
