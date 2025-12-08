from aoc25.six.solution import MathParser


def test_part_one_example():
    parser = MathParser()
    example = """123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   + """
    problems = parser.parse(example)
    assert sum(problem.solve() for problem in problems) == 4277556


def test_part_two_example():
    parser = MathParser()
    example = """123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   + """
    problems = parser.parse_part_two(example)
    assert sum(problem.solve() for problem in problems) == 3263827
