import math
from collections import deque
from functools import reduce
from typing import Callable, List, Tuple


class Graph:
    def __init__(self, size: int):
        self.edges: List[List[int]] = [list() for _ in range(size)]
        self.num_vertices = size

    def add_edge(self, source: int, target: int):
        self.edges[source].append(target)
        self.edges[target].append(source)


def bfs(graph: Graph, start: int, process: Callable[[int], None]):
    queue = deque([start])
    discovered = [False] * graph.num_vertices
    discovered[start] = True
    while queue:
        current = queue.popleft()
        process(current)
        for edge in graph.edges[current]:
            if not discovered[edge]:
                discovered[edge] = True
                queue.append(edge)


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
        # adding it to the same root, won't surpass x's other child tree ranks
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
        graph = Graph(len(self.boxes))

        # Connect the n shortest edges
        for _, node, other in self.get_distances()[:n]:
            graph.add_edge(node, other)

        # Find the distinct circuits
        circuits = []
        processed = [False] * graph.num_vertices
        for i in range(graph.num_vertices):
            # we already found this node in a circuit
            if processed[i]:
                continue

            circuit_size = 0

            def update_circuit_size(vertex: int):
                nonlocal circuit_size
                circuit_size += 1
                processed[vertex] = True

            bfs(graph, i, update_circuit_size)
            circuits.append(circuit_size)

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
