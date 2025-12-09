import dataclasses
from collections import defaultdict
from functools import lru_cache
from typing import Dict, List, Set

from aoc25.four.solution import Point


@dataclasses.dataclass(frozen=True)
class Point:
    x: int = dataclasses.field(hash=True)
    y: int = dataclasses.field(hash=True)

    def rect_area(self, other: Point) -> int:
        return (abs(self.x - other.x) + 1) * (abs(self.y - other.y) + 1)


class Floor:
    def __init__(self, red_tiles: List[Point]):
        self.red_tiles = red_tiles
        # this is a sparse map of all green tiles that can be used
        self.green_tiles: Dict[int, Set[int]] = defaultdict(set)

    def find_largest_area(self) -> int:
        # Cross product of all tiles to find the largest area - O(n**2)
        largest_area = 0
        for i, tile in enumerate(self.red_tiles):
            for j in range(i, len(self.red_tiles)):
                other = self.red_tiles[j]
                area = tile.rect_area(other)
                if area > largest_area:
                    largest_area = area

        return largest_area

    def find_largest_area_part_two(self) -> int:
        # finding the largest area where all 4 points lie within the bounding shape defined by red tiles
        # draw green tiles between points in the rows/columns, then fill with green
        if not self.red_tiles:
            return 0

        if not self.green_tiles:
            self.populate_green_border()
        # now do the cross product to find the areas, but only if all four walls are in the green area
        largest_area = 0
        for i, tile in enumerate(self.red_tiles):
            for j in range(i, len(self.red_tiles)):
                other = self.red_tiles[j]
                if self.is_rect_inside_boundary(tile, other):
                    area = tile.rect_area(other)
                    if area > largest_area:
                        largest_area = area

        return largest_area

    def populate_green_border(self):
        last_point = None
        num_tiles = len(self.red_tiles)
        for i in range(num_tiles + 1):
            # forcing it to wrap, so that it will fill the last segment
            point = self.red_tiles[i % num_tiles]
            if last_point is None:
                last_point = point
                continue
            self.fill_rect(last_point, point)
            last_point = point

    def fill_rect(self, start: Point, end: Point):
        for x in range(min(start.x, end.x), max(start.x, end.x) + 1):
            for y in range(min(start.y, end.y), max(start.y, end.y) + 1):
                self.green_tiles[x].add(y)

    def is_rect_inside_boundary(self, start: Point, end: Point) -> bool:
        # check the full border of the rectangle, so double backs are not counted
        valid = True
        for x in range(min(start.x, end.x), max(start.x, end.x) + 1):
            for y in range(min(start.y, end.y), max(start.y, end.y) + 1):
                # only check the border, not interior
                if (
                    x in (start.x, end.x) or y in (start.y, end.y)
                ) and not self.point_inside_boundary(Point(x, y)):
                    valid = False
                    break

        return valid

    @lru_cache(maxsize=None)
    def point_inside_boundary(self, p: Point) -> bool:
        if p.y in self.green_tiles[p.x]:
            return True

        walls_crossed = 0
        min_x = min([point.x for point in self.red_tiles])
        max_x = max([point.x for point in self.red_tiles])
        # Check left or right to count the walls
        for goal in (min_x, max_x):
            for x in range(min(p.x, goal), max(p.x, goal) + 1):
                # Only count vertical walls
                if p.y in self.green_tiles[x] and (
                    p.y + 1 in self.green_tiles[x] or p.y - 1 in self.green_tiles[x]
                ):
                    walls_crossed += 1

            # exit early on known success, or known fail
            if walls_crossed % 2 == 1:
                return True
            elif walls_crossed == 0:
                return False

        return False

    def draw_floor(self) -> str:
        if not self.green_tiles:
            self.populate_green_border()
        output = "\n"
        x_values = {tile.x for tile in self.red_tiles}
        max_x = max(x_values)
        y_values = {tile.y for tile in self.red_tiles}
        max_y = max(y_values)
        for y in range(0, max_y + 1):
            line = ""
            for x in range(0, max_x + 1):
                point = Point(x, y)
                if point in self.red_tiles:
                    line += "#"
                elif point.y in self.green_tiles[x]:
                    line += "@"
                elif self.point_inside_boundary(point):
                    line += "$"
                else:
                    line += "."

            output += "".join(line) + "\n"
        return output


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

    return floor.find_largest_area_part_two()


if __name__ == "__main__":
    print(run())
