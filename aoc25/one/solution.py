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
        steps = int(line[1:])
        direction = Direction.RIGHT if line.startswith('R') else Direction.LEFT
        return cls(steps, direction)


@dataclasses.dataclass
class DialConfig:
    total: int = 100


@dataclasses.dataclass
class Dial:
    loc: int
    config: DialConfig = dataclasses.field(default_factory=DialConfig)

    def rotate(self, rotation: Rotation):
        steps = rotation.steps
        if rotation.direction == Direction.LEFT:
            steps *= -1
        self.loc = (self.config.total + self.loc + steps) % self.config.total

    def points_to_zero(self) -> bool:
        return self.loc == 0


def run() -> int:
    password = 0
    dial = Dial(50)
    with open('input.txt') as f:
        for line in f.readlines():
            if not line.strip():
                continue
            rotation = Rotation.parse_rotation(line.strip())
            dial.rotate(rotation)
            if dial.points_to_zero():
                password += 1

    return password


if __name__ == '__main__':
    print(run())