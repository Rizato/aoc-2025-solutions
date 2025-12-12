from aoc25.twelve.solution import Point, Present, PresentParser


def test_present_rotation_line():
    points = {Point(0, 0), Point(5, 0)}
    present = Present(points)

    first = present.rotate()
    second = first.rotate()
    third = second.rotate()
    fourth = third.rotate()

    assert first.points == {Point(0, 0), Point(0, 5)}
    assert second.points == {Point(0, 0), Point(-5, 0)}
    assert third.points == {Point(0, 0), Point(0, -5)}
    assert fourth.points == {Point(0, 0), Point(5, 0)}


def test_present_rotation_rect():
    points = {Point(0, 0), Point(5, 0), Point(5, 3), Point(0, 3)}
    present = Present(points)
    first = present.rotate()
    second = first.rotate()
    third = second.rotate()
    fourth = third.rotate()

    assert first.points == {Point(0, 0), Point(0, 5), Point(-3, 5), Point(-3, 0)}
    assert second.points == {Point(0, 0), Point(-5, 0), Point(-5, -3), Point(0, -3)}
    assert third.points == {Point(0, 0), Point(0, -5), Point(3, -5), Point(3, 0)}
    assert fourth.points == {Point(0, 0), Point(5, 0), Point(5, 3), Point(0, 3)}


def test_present_rotation_rect_offset():
    points = {Point(0, 0), Point(5, 0), Point(5, 3), Point(0, 3)}
    present = Present(points)
    first = present.rotate(True)
    second = first.rotate(True)
    third = second.rotate(True)
    fourth = third.rotate(True)

    assert first.points == {Point(3, 0), Point(3, 5), Point(0, 5), Point(0, 0)}
    assert second.points == {Point(5, 3), Point(0, 3), Point(0, 0), Point(5, 0)}
    assert third.points == {Point(0, 5), Point(0, 0), Point(3, 0), Point(3, 5)}
    assert fourth.points == {Point(0, 0), Point(5, 0), Point(5, 3), Point(0, 3)}


def test_part_one_example():
    parser = PresentParser()
    example = """0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2"""
    presents = parser.parse(example)

    assert presents.num_can_fit() == 2


def test_part_one_example_first():
    parser = PresentParser()
    example = """0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0"""
    presents = parser.parse(example)

    assert presents.num_can_fit() == 1


def test_part_one_example_second():
    parser = PresentParser()
    example = """0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

12x5: 1 0 1 0 2 2"""
    presents = parser.parse(example)

    assert presents.num_can_fit() == 1


def test_part_one_example_third():
    parser = PresentParser()
    example = """0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

12x5: 1 0 1 0 3 2"""
    presents = parser.parse(example)

    assert presents.num_can_fit() == 0
