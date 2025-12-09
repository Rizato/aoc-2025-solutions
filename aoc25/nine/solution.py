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

        xs, ys = zip(*[(p.x, p.y) for p in self.red_tiles])
        self.x_range = (min(xs), max(xs))
        self.y_range = (min(ys), max(ys))

        self.red_tile_x_by_y: Dict[int, Set[int]] = defaultdict(set)
        for point in self.red_tiles:
            self.red_tile_x_by_y[point.y].add(point.x)

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
                if corner_a.x not in self.green_tiles[corner_a.y] or corner_b.x not in self.green_tiles[corner_b.y]:
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

        for row in range(self.y_range[0], self.y_range[1]):
            inside = True
            has_past_wall = False
            xs = self.green_tiles[row]
            started_on_up_wall = min(xs) in self.green_tiles[row - 1]
            for x in range(min(xs) + 1, max(xs) + 1):
                if inside:
                    # We found an empty spot inside, so we claim it
                    if x not in self.green_tiles[row]:
                        self.green_tiles[row].add(x)
                        # note that was are not in a wall, so we can count a horizontal segment as one wall
                        has_past_wall = True
                    else:
                        # if we hit a red tile, that isn't a wall going up, or we have passed a blank space
                        wall_direction_check = 1 if started_on_up_wall else -1
                        if has_past_wall or (x in self.red_tile_x_by_y[row] and x not in self.green_tiles[row + wall_direction_check]):
                            has_past_wall = False
                            inside = False
                else:
                    # we were not inside, and passed a wall, so now inside
                    if x in self.green_tiles[row]:
                        inside = True

    def fill_rect(self, start: Point, end: Point):
        for x in range(min(start.x, end.x), max(start.x, end.x) + 1):
            for y in range(min(start.y, end.y), max(start.y, end.y) + 1):
                self.green_tiles[y].add(x)

    def is_rect_inside_boundary(self, start: Point, end: Point) -> bool:
        # check the full border of the rectangle, so double backs are not counted
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

        return all(self.point_inside_boundary(point) for point in points)

    def point_inside_boundary(self, p: Point) -> bool:
        return p.x in self.green_tiles[p.y]

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
                elif x in self.green_tiles[point.y]:
                    line += "@"
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
