import math
from collections import deque
from functools import reduce
from typing import Callable, List, Tuple


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

    def get_shortest(self) -> List[Tuple[float, int, int]]:
        distances: List[Tuple[float, int, int]] = []
        for i, source in enumerate(self.vertices):
            for j in range(i + 1, len(self.vertices)):
                target = self.vertices[j]
                distances.append((source.distance(target), i, j))
        # sort from shortest to longest, and take n connections
        return sorted(distances, key=lambda x: x[0])

    def create_single_circuit(self) -> int:
        connections = deque(self.get_shortest())
        connected = [False] * self.num_vertices

        # start a circuit on the first connection
        first = True
        last_source = 0
        last_target = 0

        def mark_connected(vertex: int):
            connected[vertex] = True

        while connections and not all(connected):
            _, source, target = connections.popleft()
            last_source = source
            last_target = target
            if first:
                connected[source] = True
                connected[target] = True
                first = False

            if connected[target] and not connected[source]:
                bfs(self, source, mark_connected)

            if connected[source] and not connected[target]:
                bfs(self, target, mark_connected)

            # add edge to graph
            self.edges[source].append(target)
            self.edges[target].append(source)

        # Result is the product of the last connected vertices x values
        return self.vertices[last_source].x * self.vertices[last_target].x

    def connect_n_shortest(self, n: int) -> int:
        # Connect the n shortest edges
        for _, node, other in self.get_shortest()[:n]:
            self.edges[node].append(other)
            self.edges[other].append(node)

        # Find the distinct circuits
        circuits = []
        processed = [False] * self.num_vertices
        for i in range(self.num_vertices):
            # we already found this node in a circuit
            if processed[i]:
                continue

            circuit_size = 0

            def update_circuit_size(vertex: int):
                nonlocal circuit_size
                circuit_size += 1
                processed[vertex] = True

            bfs(self, i, update_circuit_size)
            circuits.append(circuit_size)

        top_three = (
            sorted(circuits, reverse=True)[:3] if len(circuits) >= 3 else circuits
        )
        return reduce(lambda x, y: x * y, top_three)


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

    return graph.create_single_circuit()


if __name__ == "__main__":
    print(run())
