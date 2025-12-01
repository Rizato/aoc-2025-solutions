import dataclasses
import enum
from typing import Self


class Direction(enum.Enum):
    LEFT = enum.auto()
    RIGHT = enum.auto()


@dataclasses.dataclass(frozen=True)
class Rotation:
    steps: int
    direction: Direction

    @classmethod
    def parse_rotation(cls, line: str) -> Self:
        if len(line) < 2:
            raise ValueError

        steps = int(line[1:])
        direction = Direction.LEFT if line.startswith("L") else Direction.RIGHT
        return cls(steps, direction)


@dataclasses.dataclass
class Dial:
    loc: int
    size: int

    def rotate_tracking_passes(self, rotation: Rotation) -> int:
        passes = self.calculate_zero_passes(rotation)
        self.rotate(rotation)
        return passes

    def calculate_zero_passes(self, rotation: Rotation) -> int:
        start = self.loc
        steps = rotation.steps

        distance_to_zero = (
            start or self.size
            if rotation.direction == Direction.LEFT
            else self.size - start
        )

        passes = 0
        while steps >= distance_to_zero:
            passes += 1
            steps -= distance_to_zero
            distance_to_zero = self.size

        return passes

    def rotate(self, rotation: Rotation):
        steps = rotation.steps
        if rotation.direction == Direction.LEFT:
            steps *= -1
        self.loc = (self.size + self.loc + steps) % self.size

    def points_to_zero(self) -> bool:
        return self.loc == 0


def run() -> int:
    password = 0
    dial = Dial(50, 100)
    with open("input.txt") as f:
        for line in f.readlines():
            if not line.strip():
                continue
            rotation = Rotation.parse_rotation(line.strip())
            password += dial.rotate_tracking_passes(rotation)

    return password


if __name__ == "__main__":
    print(run())
