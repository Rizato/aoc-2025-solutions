from aoc25.four.solution import DepartmentFloor


def test_part_one_example():
    floor = DepartmentFloor()
    example = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""
    floor.populate_floor(example)
    assert floor.get_removable_rolls(4) == 13


def test_part_two_example():
    floor = DepartmentFloor()
    example = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""
    floor.populate_floor(example)
    assert floor.remove_all_rolls(4) == 43
