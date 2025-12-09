import dataclasses
from typing import List


@dataclasses.dataclass(frozen=True)
class Point:
    x: int
    y: int


class Floor:
    def __init__(self, red_tiles: List[Point]):
        self.red_tiles = red_tiles

    def find_largest_area(self) -> int:
        # Cross product of all tiles to find the largest area?
        largest_area = 0
        for i, tile in enumerate(self.red_tiles):
            for j in range(i, len(self.red_tiles)):
                other = self.red_tiles[j]
                area = abs(tile.x - other.x + 1) * abs(tile.y - other.y + 1)
                if area > largest_area:
                    largest_area = area

        return largest_area


class RedTileParser:

    @staticmethod
    def parse(junctions: str) -> Floor:
        red_tiles = []
        for line in junctions.splitlines():
            if not line.strip():
                continue

            coordinates = line.split(",")
            tile = Point(int(coordinates[0]), int(coordinates[1]))
            red_tiles.append(tile)

        return Floor(red_tiles)


def run() -> int:

    with open("input.txt", "r") as f:
        floor = RedTileParser().parse(f.read())

    return floor.find_largest_area()


if __name__ == "__main__":
    print(run())
