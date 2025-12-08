import math
from collections import deque
from functools import reduce
from typing import List, Tuple


class Vertex:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def distance(self, other: "Vertex") -> float:
        dist_sq = (
            pow(self.x - other.x, 2)
            + pow(self.y - other.y, 2)
            + pow(self.z - other.z, 2)
        )
        return math.sqrt(dist_sq)


class Graph:
    def __init__(self):
        self.vertices: List[Vertex] = []
        self.edges: List[List[int]] = []
        self.num_vertices = 0

    def add_vertex(self, graph_node: Vertex):
        self.vertices.append(graph_node)
        self.edges.append(list())
        self.num_vertices += 1

    def get_n_shortest(self, n: int) -> List[Tuple[float, int, int]]:
        distances: List[Tuple[float, int, int]] = []
        for i, node in enumerate(self.vertices):
            for j in range(i + 1, len(self.vertices)):
                other = self.vertices[j]
                distances.append((node.distance(other), i, j))
        # sort from shortest to longest, and take n connections
        return sorted(distances, key=lambda x: x[0])[:n]

    def connect_n_shortest(self, n: int) -> int:
        # Connect the n shortest edges
        for _, node, other in self.get_n_shortest(n):
            self.edges[node].append(other)
            self.edges[other].append(node)

        # now we have populated our graph, so find all the distinct sub-groups
        # bfs across the graph starting from each vertex
        circuits = []
        processed = [False] * self.num_vertices
        discovered = [False] * self.num_vertices
        for i in range(self.num_vertices):

            # we already found this node in a circuit
            if processed[i]:
                continue

            # track how many vertices in this circuit
            size = 0
            queue = deque([i])
            discovered[i] = True
            while queue:
                vertex = queue.popleft()
                processed[vertex] = True
                size += 1
                for edge in self.edges[vertex]:
                    if not discovered[edge] and not processed[edge]:
                        discovered[edge] = True
                        queue.append(edge)

            circuits.append(size)

        top_three = (
            sorted(circuits, reverse=True)[:3] if len(circuits) >= 3 else circuits
        )
        return reduce(lambda x, y: x * y, top_three)


class JunctionParser:

    @staticmethod
    def parse(junctions: str) -> Graph:
        graph = Graph()
        for line in junctions.splitlines():
            if not line.strip():
                continue

            coordinates = line.split(",")
            vertex = Vertex(
                int(coordinates[0]), int(coordinates[1]), int(coordinates[2])
            )
            graph.add_vertex(vertex)

        return graph


def run() -> int:

    with open("input.txt", "r") as f:
        graph = JunctionParser().parse(f.read())

    return graph.connect_n_shortest(1000)


if __name__ == "__main__":
    print(run())
