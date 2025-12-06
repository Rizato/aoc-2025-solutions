import dataclasses
import enum
from functools import reduce
from typing import List

class Operator(enum.Enum):
    ADD = enum.auto()
    MULTIPLY = enum.auto()


@dataclasses.dataclass
class MathProblem:
    values: List[int] = dataclasses.field(default_factory=list)
    operator: Operator = Operator.ADD

    def solve(self) -> int:
        return reduce(lambda x, y: x * y if self.operator == Operator.MULTIPLY else x + y , self.values)


class MathParser:

    @staticmethod
    def parse(math_problems: str) -> List[MathProblem]:
        problems = []
        for line in math_problems.splitlines():
            # This could cause issues if it doesn't remove all whitespace
            column = 0
            for value in line.split(" "):
                if not value.strip():
                    continue

                if column >= len(problems):
                    problems.append(MathProblem())

                if value == "*":
                    problems[column].operator = Operator.MULTIPLY
                elif value == "+":
                    problems[column].operator = Operator.ADD
                else:
                    problems[column].values.append(int(value))

                column += 1


        return problems


def run() -> int:

    with open("input.txt", "r") as f:
        problems = MathParser().parse(f.read())

    return sum(problem.solve() for problem in problems)


if __name__ == "__main__":
    print(run())
