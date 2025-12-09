import dataclasses
from collections import defaultdict
from typing import Dict, List, Set

from aoc25.four.solution import Point


@dataclasses.dataclass(frozen=True)
class Point:
    x: int
    y: int

    def rect_area(self, other: Point) -> int:
        return (abs(self.x - other.x) + 1) * (abs(self.y - other.y) + 1)


class Floor:
    def __init__(self, red_tiles: List[Point]):
        self.red_tiles = red_tiles

    def find_largest_area(self) -> int:
        # Cross product of all tiles to find the largest area
        # O(n**2)
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
        # basically you have to have at least 3 red corners, and the fourth corner should be red or green

        # Create a map of points for fast column/row lookups
        # I figure the points will be very large, so we are making a bucketed sparse array
        x_to_ys: Dict[int, Set[int]] = defaultdict(set)
        y_to_xs: Dict[int, Set[int]] = defaultdict(set)

        for tile in self.red_tiles:
            x_to_ys[tile.x].add(tile.y)
            y_to_xs[tile.y].add(tile.x)

        # create the boundary by drawing vertical & lines to all points in a row/column
        green_x_to_ys: Dict[int, Set[int]] = defaultdict(set)
        for tile in self.red_tiles:
            # create a green bar for this column
            ys = x_to_ys[tile.x]
            # make all green, inclusive
            for i in range(min(ys), max(ys) + 1):
                green_x_to_ys[tile.x].add(i)

            # create a green bar for this row
            xs = y_to_xs[tile.y]
            # make all green, inclusive
            for i in range(min(xs), max(xs) + 1):
                green_x_to_ys[i].add(tile.y)

        # I missed that the fourth point must appear inside the area as well. So, if we create a phantom fourth point, how do we test?
        largest_area = 0
        for tile in self.red_tiles:
            # see if it is a pivot
            if len(x_to_ys[tile.x]) > 1 and len(y_to_xs[tile.y]) > 1:
                # find all the points matching both axes (but not self)
                matching_x_points = [
                    Point(tile.x, y) for y in x_to_ys[tile.x] if y != tile.y
                ]
                matching_y_points = [
                    Point(x, tile.y) for x in y_to_xs[tile.y] if x != tile.x
                ]
                # compute the area of all matching points, to find the largest possible
                for x in matching_x_points:
                    for y in matching_y_points:
                        if x.rect_area(y) > largest_area:
                            # get the corner opposite the pivot
                            fourth_point_x = x.x if x.x != tile.x else y.x
                            fourth_point_y = x.y if x.y != tile.x else y.y
                            # check if the last point is contained in the bounding area
                            ys = green_x_to_ys[fourth_point_x]
                            if min(ys) <= fourth_point_y <= max(ys):
                                largest_area = x.rect_area(y)
                            else:
                                pass

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

    return floor.find_largest_area_part_two()


if __name__ == "__main__":
    print(run())
