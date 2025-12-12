import dataclasses
from functools import lru_cache
from typing import List, NamedTuple, Tuple


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
    points: Tuple[Point, ...]

    @property
    def size(self) -> int:
        return len(self.points)

    @property
    def width(self) -> int:
        return max(p.x for p in self.points)

    def offset(self, offset: Point) -> "Present":
        """Given some offset, compute all the new points and return"""
        return Present(tuple(p.add(offset) for p in self.points))

    def rotate(self, with_offset: bool = False) -> "Present":
        """rotates the present 90 degrees clockwise"""
        # negate the y position and swap
        rotated = Present(tuple(Point(-p.y, p.x) for p in self.points))
        if not with_offset:
            return rotated

        # offset so that every point is only positive integers
        low_x = min(p.x for p in rotated.points)
        low_y = min(p.y for p in rotated.points)
        offset_x = -low_x if low_x < 0 else 0
        offset_y = -low_y if low_y < 0 else 0
        offset = Point(offset_x, offset_y)
        return rotated.offset(offset)

    @lru_cache(maxsize=None)
    def all_rotations(self) -> Tuple["Present", ...]:
        rotations = []
        current = self
        for _ in range(3):
            rotations.append(current)
            current = current.rotate(True)
        return tuple(rotations)


@dataclasses.dataclass(frozen=True)
class Region:
    width: int
    height: int
    num_required_presents: List[int]

    @property
    def area(self) -> int:
        return self.width * self.height

    def can_fit(self, presents: List[Present]) -> bool:
        # this solution is O(n * m * k), where n is the number of shapes (*4 for rotations) * area of the region * total number of shapes to match
        # first pass, just count if there are enough tiles to literally fit everything
        @lru_cache(maxsize=None)
        def enough_tiles(required_presents: Tuple[int, ...], available: int) -> bool:
            consumed = sum(
                presents[present].size * num_required
                for present, num_required in enumerate(required_presents)
                if num_required > 0
            )
            return consumed <= available

        if not enough_tiles(tuple(self.num_required_presents), self.area):
            return False

        # do dfs brute force
        def fit_present(
            required_presents: List[int], available_points: List[Point], index: int
        ) -> bool:
            # check if there are even enough points left to fit the shape
            present = presents[index]
            if len(available_points) < present.size or not enough_tiles(
                tuple(required_presents), len(available_points)
            ):
                return False

            # calculate this once per test, it just tells us the next present to test based on shape size
            next_required = required_presents.copy()
            next_required[index] -= 1
            next_present = None
            if sum(next_required) > 0:
                # sort largest to smallest
                sorted_required = sorted(
                    enumerate(next_required),
                    key=lambda p: presents[p[0]].size,
                    reverse=True,
                )
                next_present = [
                    i for i, requirement in sorted_required if requirement > 0
                ][0]
            # can_check gives us the excess, if there is 0 excess we could still fit, so check for one
            can_check = len(available_points) - present.size
            for offset in available_points[: can_check + 1]:
                # for each rotation of the shape
                for rotation in present.all_rotations():
                    offset_preset = rotation.offset(offset)
                    # if we fit, continue down the stack if there are more to fit
                    if all(point in available_points for point in offset_preset.points):
                        # if there are no more presents to fit, we can return true
                        if not next_present:
                            return True

                        next_available_points = available_points.copy()
                        # remove all the points for the next step
                        for point in offset_preset.points:
                            next_available_points.remove(point)

                        # test the largest present remaining
                        if next_present and fit_present(
                            next_required, next_available_points, next_present
                        ):
                            return True

            # if we didn't find a solution, return false
            return False

        # call the function with each of the starting shapes
        points = [Point(x, y) for x in range(self.width) for y in range(self.height)]
        # act on each as a starting point in the dfs
        for i, required in sorted(
            enumerate(self.num_required_presents),
            key=lambda p: presents[p[0]].size,
            reverse=True,
        ):
            if required > 0:
                return fit_present(self.num_required_presents, points, i)
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

        points = list()
        for y, line in enumerate(present.splitlines()[1:]):
            for x, character in enumerate(line):
                if character == "#":
                    points.append(Point(x, y))

        return Present(tuple(points))

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
