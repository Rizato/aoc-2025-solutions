import dataclasses
import enum
from collections import deque
from functools import reduce
from typing import Generator, List, Optional


class Operator(enum.Enum):
    ADD = enum.auto()
    MULTIPLY = enum.auto()


@dataclasses.dataclass
class MathProblem:
    operands: List[int] = dataclasses.field(default_factory=list)
    operator: Operator = Operator.ADD

    def solve(self) -> int:
        return reduce(
            lambda x, y: x * y if self.operator == Operator.MULTIPLY else x + y,
            self.operands,
        )


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
                    problems[column].operands.append(int(value))

                column += 1

        return problems

    def parse_part_two(self, math_problems: str) -> Generator[MathProblem, None, None]:
        operands: List[Optional[int]] = []
        operators = deque()
        for line in math_problems.splitlines():
            if not operands:
                # Includes an extra None for the last group to be calculated
                operands = [None] * (len(line) + 1)
            for i, value in enumerate(line):
                if not value.strip():
                    continue

                if value.isdigit():
                    # Update the corresponding spot with the new value
                    if operands[i] is None:  # none check, in case 0
                        operands[i] = int(value)
                    else:
                        operands[i] *= 10
                        operands[i] += int(value)
                else:
                    operators.append(
                        Operator.ADD if value == "+" else Operator.MULTIPLY
                    )

        # group all
        current = []
        for value in operands:
            if value:
                current.append(value)
            elif current:
                # yield the current math problem
                yield MathProblem(current, operators.popleft())
                current.clear()


def run() -> int:

    with open("input.txt", "r") as f:
        problems = MathParser().parse_part_two(f.read())

    return sum(problem.solve() for problem in problems)


if __name__ == "__main__":
    print(run())
