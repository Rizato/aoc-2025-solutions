import dataclasses
import enum
from typing import Iterable, Self


class Tile(enum.Enum):
    """Represents an object on the layout floor"""

    EMPTY = enum.auto()
    ROLL = enum.auto()


@dataclasses.dataclass
class Point:
    x: int
    y: int

    def add(self, point: "Point") -> Self:
        new_x = self.x + point.x
        new_y = self.y + point.y
        return Point(new_x, new_y)


class DepartmentFloor:

    def __init__(self):
        self.width = 0
        self.floor_spaces = []
        self.num_adjacent = []

    def get_available_rolls(self, max_adjacent: int) -> int:
        return sum(
            1
            for num, space in zip(self.num_adjacent, self.floor_spaces)
            if space == Tile.ROLL and num < max_adjacent
        )

    def populate_floor(self, layout: Iterable[str]):
        # negative one, just so the index adding is near the loop for readability
        index = -1
        for line in layout.split("\n"):
            if not line.strip():
                continue

            # will be set to the line length
            if self.width == 0:
                self.width = len(line)

            for char in line:
                # Update index before processing
                index += 1
                if char == ".":
                    self.floor_spaces.append(Tile.EMPTY)
                    # don't car about adjacent non-floor spaces
                    self.num_adjacent.append(0)
                else:
                    # Mark floor as a paper spot
                    self.floor_spaces.append(Tile.ROLL)
                    self.num_adjacent.append(0)
                    p = self.get_point(index)
                    # check nw, n, ne, w
                    checks = [(-1, -1), (0, -1), (1, -1), (-1, 0)]
                    for diff_x, diff_y in checks:
                        to_check = p.add(Point(diff_x, diff_y))
                        if to_check.x < 0 or to_check.x >= self.width or to_check.y < 0:
                            continue

                        to_check_index = self.get_index(to_check)
                        if self.floor_spaces[to_check_index] == Tile.ROLL:
                            # increment our adjacent count, and it's
                            self.num_adjacent[to_check_index] += 1
                            self.num_adjacent[index] += 1

    def get_index(self, point: Point) -> int:
        return point.y * self.width + point.x

    def get_point(self, index: int) -> Point:
        x = index % self.width
        y = index // self.width
        return Point(x, y)


def run() -> int:
    printing_department = DepartmentFloor()
    with open("input.txt", "r") as f:
        printing_department.populate_floor(f.read())

    return printing_department.get_available_rolls(4)


if __name__ == "__main__":
    print(run())
