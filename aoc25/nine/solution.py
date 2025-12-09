import dataclasses
from collections import defaultdict
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
        self.walls_crossed_left: Dict[Point, int] = defaultdict(int)
        self.walls_crossed_right: Dict[Point, int] = defaultdict(int)

        xs, ys = zip(*[(p.x, p.y) for p in self.red_tiles])
        self.x_range = (min(xs), max(xs))
        self.y_range = (min(ys), max(ys))

        self.inside: Dict[Point, bool] = {}

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
                area = tile.rect_area(other)
                corner_a = Point(tile.x, other.y)
                corner_b = Point(other.x, tile.y)
                if corner_a.y not in self.green_tiles[corner_a.x] or corner_b.y not in self.green_tiles[corner_b.x]:
                    continue

                if area > largest_area and self.is_rect_inside_boundary(tile, other):
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
        points = []
        min_x = min(start.x, end.x)
        max_x = max(start.x, end.x)
        min_y = min(start.y, end.y)
        max_y = max(start.y, end.y)
        # add top and bottom
        for y in (min_y, max_y):
            for x in range(min_x, max_x + 1):
                points.append(Point(x, y))

        # add left and right
        for x in (min_x, max_x):
            for y in range(min_y, max_y + 1):
                points.append(Point(x, y))

        for point in points:
            # only check the border, not interior to save time
            if not self.point_inside_boundary(point):
                valid = False
                break

        return valid

    def point_inside_boundary(self, p: Point) -> bool:
        if p.x == 7 and p.y == 1:
            pass

        if p in self.inside:
            return self.inside[p]

        min_x, max_x = self.x_range
        min_y, max_y = self.y_range
        if p.x < min_x or p.x > max_x or p.y < min_y or p.y > max_y:
            self.inside[p] = False
            return False

        if p.y in self.green_tiles[p.x]:
            self.inside[p] = True
            return True

        inside = False
        for cache, target in (
            (self.walls_crossed_left, min_x),
            (self.walls_crossed_right, max_x),
        ):
            walls_crossed = self.num_walls_crossed(cache, p, target)

            if walls_crossed % 2 == 1:
                inside = True
            elif walls_crossed == 0:
                self.inside[p] = False
                return False

        self.inside[p] = inside
        return inside

    def num_walls_crossed(
        self, cache: Dict[Point, int], p: Point, target_x: int
    ) -> int:
        if p in cache:
            return cache[p]

        step = 1 if p.x > target_x else -1
        for x in range(target_x, p.x + step, step):
            # skip to unknown
            if Point(x, p.y) in cache:
                continue

            previous = cache[Point(x - step, p.y)] if x > 0 else 0
            is_vertical_wall = p.y in self.green_tiles[x] and (
                p.y + 1 in self.green_tiles[x] or p.y - 1 in self.green_tiles[x]
            )
            cache[Point(x, p.y)] = (1 if is_vertical_wall else 0) + previous

        return cache[p]

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
