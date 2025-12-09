import math
from collections import defaultdict, deque
from functools import reduce
from typing import Dict, List, Tuple


class UnionFind:
    def __init__(self, size: int):
        self.parents = [i for i in range(size)]
        self.rank = [1] * size

    def find(self, query: int) -> int:
        # recursive search to find the parent of my parent
        if self.parents[query] != query:
            # this is known as path compression (because we only store the final parent)
            self.parents[query] = self.find(self.parents[query])
            return self.parents[query]

        return query

    def union(self, a: int, b: int):
        x = self.find(a)
        y = self.find(b)
        # same parent, means same group
        if x == y:
            return

        # make sure x is always the greater rank
        if self.rank[x] < self.rank[y]:
            x, y = y, x

        # set the parent
        self.parents[y] = x
        # Only increase rank if they are the same, because stacking them increases the height by one
        # However, when y is smaller (which is forced to be smaller or equal by the swap above),
        # the minimum rank of x after adding y is rank of y + 1, which is at most equal to the existing rank of x
        if self.rank[x] == self.rank[y]:
            self.rank[x] += 1

    def all_connected(self) -> bool:
        return len(set([self.find(i) for i in range(len(self.parents))])) == 1


class JunctionBox:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def distance(self, other: "JunctionBox") -> float:
        dist_sq = (
            pow(self.x - other.x, 2)
            + pow(self.y - other.y, 2)
            + pow(self.z - other.z, 2)
        )
        return math.sqrt(dist_sq)


class JunctionBoxes:
    def __init__(self, boxes: List[JunctionBox]):
        self.boxes = boxes
        self.distances = []

    def connect_n_shortest(self, n: int) -> int:
        unionfind = UnionFind(len(self.boxes))

        # Connect the n shortest edges
        for _, node, other in self.get_distances()[:n]:
            unionfind.union(node, other)

        circuits = [0] * len(self.boxes)

        for i in range(len(self.boxes)):
            circuits[unionfind.find(i)] += 1

        top_three = (
            sorted(circuits, reverse=True)[:3] if len(circuits) >= 3 else circuits
        )

        return reduce(lambda x, y: x * y, top_three)

    def find_product_of_last_connection(self) -> int:
        unionfind = UnionFind(len(self.boxes))
        connections = deque(self.get_distances())

        source, target = 0, 0
        while connections and not unionfind.all_connected():
            _, source, target = connections.popleft()
            unionfind.union(source, target)

        # Result is the product of the last connected vertices x values
        return self.boxes[source].x * self.boxes[target].x

    def get_distances(self) -> List[Tuple[float, int, int]]:
        if self.distances:
            return self.distances
        distances: List[Tuple[float, int, int]] = []
        for i, source in enumerate(self.boxes):
            for j in range(i + 1, len(self.boxes)):
                target = self.boxes[j]
                distances.append((source.distance(target), i, j))
        # sort from shortest to longest, and take n connections
        self.distances = sorted(distances, key=lambda x: x[0])
        return self.distances


class JunctionParser:

    @staticmethod
    def parse(junctions: str) -> JunctionBoxes:
        vertices = []
        for line in junctions.splitlines():
            if not line.strip():
                continue

            coordinates = line.split(",")
            vertex = JunctionBox(
                int(coordinates[0]), int(coordinates[1]), int(coordinates[2])
            )
            vertices.append(vertex)

        return JunctionBoxes(vertices)


def run() -> int:

    with open("input.txt", "r") as f:
        boxes = JunctionParser().parse(f.read())

    return boxes.find_product_of_last_connection()


if __name__ == "__main__":
    print(run())
