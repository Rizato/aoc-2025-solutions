import dataclasses
from collections import defaultdict
from typing import Dict, List, Set, Tuple

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

        self.polygon_x_ranges_by_y: Dict[int, List[Tuple[int, int]]] = defaultdict(list)

        xs, ys = zip(*[(p.x, p.y) for p in self.red_tiles])
        self.x_range = (min(xs), max(xs))
        self.y_range = (min(ys), max(ys))

        self.scanned_rows = set()

        self.red_tile_x_by_y: Dict[int, Set[int]] = defaultdict(set)
        self.red_tile_y_by_x: Dict[int, Set[int]] = defaultdict(set)
        for point in self.red_tiles:
            self.red_tile_x_by_y[point.y].add(point.x)
            self.red_tile_y_by_x[point.x].add(point.y)

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
        areas: List[Tuple[int, Point, Point]] = []
        for i, tile in enumerate(self.red_tiles):
            for j in range(i, len(self.red_tiles)):
                other = self.red_tiles[j]
                area = tile.rect_area(other)
                areas.append((area, tile, other))
        areas = sorted(areas, key=lambda x: x[0], reverse=True)
        for area, tile, other in areas:
            corner_a = Point(tile.x, other.y)
            corner_b = Point(other.x, tile.y)

            if not self.point_inside_boundary(
                corner_a
            ) or not self.point_inside_boundary(corner_b):
                continue

            if self.is_rect_inside_boundary(tile, other):
                return area

        return 0

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
        if p.x in self.green_tiles[p.y]:
            return True

        # quick fail for points that cannot be in the polygon
        existing_points = sorted(self.green_tiles[p.y])
        if (
            not existing_points
            or p.x < min(existing_points)
            or p.x > max(existing_points)
        ):
            return False

        # instead of scanning each value, define ranges in the row that are inside vs outside, then do a comparison

        self.scan_row(p.y)
        # scan ranges for the row
        x_ranges = self.polygon_x_ranges_by_y[p.y]
        return any((True for lower, upper in x_ranges if lower <= p.x <= upper))

    def scan_row(self, row: int):
        if row in self.scanned_rows:
            return

        self.scanned_rows.add(row)
        inside = True
        has_past_wall = False
        xs = []
        xs.extend(self.red_tile_x_by_y[row])
        xs.extend(self.green_tiles[row])
        if not xs:
            return

        is_vertical_corner = (
            min(xs) not in self.green_tiles[row - 1]
            or min(xs) not in self.green_tiles[row + 1]
        )
        started_bottom_corner = min(xs) in self.green_tiles[row - 1]
        # This is too slow, it needs to do a comparison instead of calculating all values
        last_x = None
        # a list of inside the polygon ranges, inclusive
        inside_ranges: List[Tuple[int, int]] = []
        range_start = None

        for x in sorted(set(xs)):
            if last_x is None:
                last_x = x
                continue

            # iterate on red tiles, and green tiles
            if inside:
                # Start the range when we go inside
                if range_start is None:
                    range_start = last_x

                # we have hit a gap (lets us count horizontal segments as a single wall)
                if last_x + 1 != x:
                    has_past_wall = True

                # if we hit a red tile, that isn't a wall going up, or we have passed a blank space
                wall_direction_check = 1 if started_bottom_corner else -1
                if has_past_wall or (
                    x in self.red_tile_x_by_y[row]
                    and is_vertical_corner
                    and x not in self.green_tiles[row + wall_direction_check]
                ):
                    has_past_wall = False
                    inside = False
                    inside_ranges.append((range_start, x))
                    range_start = None
            else:
                # we were not inside, and passed a wall, so now inside
                inside = True
                is_vertical_corner = (
                    x not in self.green_tiles[row - 1]
                    or x not in self.green_tiles[row + 1]
                )
                started_bottom_corner = x in self.green_tiles[row - 1]
            last_x = x

        self.polygon_x_ranges_by_y[row].extend(inside_ranges)

    def draw_floor(self) -> str:
        if not self.green_tiles:
            self.populate_green_border()
        output = "\n"
        x_values = {tile.x for tile in self.red_tiles}
        max_x = max(x_values)
        y_values = {tile.y for tile in self.red_tiles}
        max_y = max(y_values)
        for y in range(0, max_y + 1):
            self.scan_row(y)
            line = ""
            for x in range(0, max_x + 1):
                point = Point(x, y)
                if point in self.red_tiles:
                    line += "#"
                elif x in self.green_tiles[point.y]:
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
