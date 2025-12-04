from aoc25.four.solution import DepartmentFloor


def test_part_one_example():
    floor = DepartmentFloor()
    example = """
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
"""
    floor.populate_floor(example)
    assert floor.get_available_rolls(4) == 13
