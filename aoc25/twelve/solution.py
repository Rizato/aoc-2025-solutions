import dataclasses
from functools import lru_cache
from typing import List, NamedTuple, Set


class Point(NamedTuple):
    x: int
    y: int

    @lru_cache(maxsize=None)
    def add(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    @lru_cache(maxsize=None)
    def swap(self) -> "Point":
        return Point(self.y, self.x)


@dataclasses.dataclass(frozen=True)
class Present:
    points: Set[Point]

    @property
    def size(self) -> int:
        return len(self.points)

    @property
    def width(self) -> int:
        return max(p.x for p in self.points)

    def offset(self, offset: Point) -> "Present":
        """Given some offset, compute all the new points and return"""
        return Present({p.add(offset) for p in self.points})

    def rotate(self, with_offset: bool = False) -> "Present":
        """rotates the present 90 degrees clockwise"""
        # negate the y position and swap
        rotated = Present({Point(-p.y, p.x) for p in self.points})
        if not with_offset:
            return rotated

        # offset so that every point is only positive integers
        low_x = min(p.x for p in rotated.points)
        low_y = min(p.y for p in rotated.points)
        offset_x = -low_x if low_x < 0 else 0
        offset_y = -low_y if low_y < 0 else 0
        offset = Point(offset_x, offset_y)
        return rotated.offset(offset)

    def all_rotations(self) -> List["Present"]:
        rotations = []
        current = self
        for _ in range(3):
            rotations.append(current)
            current = current.rotate(True)
        return rotations


@dataclasses.dataclass(frozen=True)
class Region:
    width: int
    height: int
    num_required_presents: List[int]

    @property
    def area(self) -> int:
        return self.width * self.height

    def can_fit(self, presents: List[Present]) -> bool:

        # first pass, just count if there are enough tiles to literally fit everything
        consumed = 0
        for i, shape in enumerate(presents):
            # consume size * number of tiles required
            consumed += shape.size * self.num_required_presents[i]
        if consumed > self.area:
            return False

        # do dfs brute force
        def fit_present(
            required_presents: List[int], available_points: Set[Point], index: int
        ) -> bool:
            present = presents[index]
            # check if there are even enough points left to fit the shape
            if len(available_points) < present.size:
                return False

            # for each rotation of the shape
            for rotation in present.all_rotations():
                # for each point, check if all the points required by the offset shape are still available
                for offset in available_points:
                    offset_preset = rotation.offset(offset)
                    # if we fit, continue down the stack if there are more to fit
                    if all(point in available_points for point in offset_preset.points):
                        next_required = required_presents.copy()
                        next_required[index] -= 1
                        # if there are no more presents to fit, we can return true
                        if sum(next_required) == 0:
                            return True

                        next_available_points = available_points.copy()
                        # remove all the points for the next step
                        for point in offset_preset.points:
                            next_available_points.remove(point)

                        # otherwise, continue down the list. continue to go down the list, or return true if required_presents is empty
                        for i, num_left in enumerate(next_required):
                            if num_left == 0:
                                continue
                            # update required, update available, get new present
                            if fit_present(next_required, next_available_points, i):
                                return True

            # if we didn't find a solution, return false
            return False

        # call the function with each of the starting shapes
        point_set = {Point(x, y) for x in range(self.width) for y in range(self.height)}
        # act on each as a starting point in the dfs
        for i, required in enumerate(self.num_required_presents):
            if required > 0:
                if fit_present(self.num_required_presents, point_set, i):
                    return True

        return False


@dataclasses.dataclass(frozen=True)
class TreeFarm:
    presents: List[Present]
    regions: List[Region]

    def num_can_fit(self) -> int:
        total = 0
        for region in self.regions:
            if region.can_fit(self.presents):
                total += 1
        return total


class PresentParser:

    @staticmethod
    def parse(tree_farm: str) -> TreeFarm:
        presents = []
        regions = []
        # start parsing presents
        parsing_presents = True
        # split on double newlines, as that separates sections
        for section in tree_farm.split("\n\n"):
            if not section.strip():
                continue

            # the regions format always has x in it
            if parsing_presents and "x" in section:
                parsing_presents = False

            if parsing_presents:
                # have to pase the entire shape representation
                presents.append(PresentParser.parse_present(section))
            else:
                # regions are easy, as they are oneline a peice
                regions.extend(
                    [
                        PresentParser.parse_region(line)
                        for line in section.splitlines()
                        if line.strip()
                    ]
                )

        return TreeFarm(presents, regions)

    @staticmethod
    def parse_present(present: str) -> Present:
        # first line is just the index, and the given input is in order, so we don't care
        if not present.strip():
            raise ValueError("empty present")

        points = set()
        for y, line in enumerate(present.splitlines()[1:]):
            for x, character in enumerate(line):
                if character == "#":
                    points.add(Point(x, y))

        return Present(points)

    @staticmethod
    def parse_region(line: str) -> Region:
        x_index = line.index("x")
        colon_index = line.index(":")
        width = int(line.strip()[:x_index])
        height = int(line.strip()[x_index + 1 : colon_index])
        presents = []
        # not enumerate for case of empty substr
        count = 0
        for p in line[colon_index + 1 :].split(" "):
            stripped = p.strip()
            if not stripped:
                continue

            presents.append(int(stripped))
            count += 1

        return Region(width, height, presents)


def run() -> int:

    with open("input.txt", "r") as f:
        presents = PresentParser().parse(f.read())

    return presents.num_can_fit()


if __name__ == "__main__":
    print(run())
