import dataclasses
from collections import deque
from typing import Dict, List, Optional


@dataclasses.dataclass
class EdgeNode:
    vertex: int
    next_edge: Optional["EdgeNode"] = None

    def __iter__(self) -> "EdgeNodeInterator":
        return EdgeNodeInterator(self)


class EdgeNodeInterator:
    def __init__(self, edge: EdgeNode):
        self.edge = edge

    def __next__(self):
        edge = self.edge
        if not edge:
            raise StopIteration

        self.edge = edge.next_edge
        return edge


class Graph:
    edges: List[Optional[EdgeNode]]
    num_vertices: int
    num_edges: int

    def __init__(self, num_vertices: int):
        # initialized all the point back to self
        self.edges = [None] * num_vertices
        self.num_edges = 0
        self.num_vertices = num_vertices

    def add_edge(self, vertex: int, target: int):
        if vertex > self.num_vertices:
            raise IndexError

        edge = EdgeNode(target, self.edges[vertex])
        edge.next_edge = self.edges[vertex]
        self.edges[vertex] = edge
        self.num_edges += 1


class Network:
    vertices: List[str]
    graph: Graph

    def __init__(self, vertices: List[str], graph: Graph):
        self.vertices = vertices
        self.graph = graph

    def find_paths(self, start: str, end: str) -> int:
        # dfs to find all paths that lead to the out node
        source = self.vertices.index(start)
        dest = self.vertices.index(end)
        paths = 0
        stack = deque([edge.vertex for edge in list(self.graph.edges[source])])
        while stack:
            current = stack.popleft()
            if current == dest:
                paths += 1
                continue

            # We got back to self, so don't process anymore
            if current == source:
                continue

            if self.graph.edges[current]:
                for neighbor in self.graph.edges[current]:
                    # don't add self, which is the start
                    if neighbor.vertex != current:
                        stack.append(neighbor.vertex)

        return paths

    def find_dac_fft_paths(self, start: str, end: str, requirements: List[str]) -> int:
        # wait, do I just count how many paths to fft,
        # then paths to dac, then paths to out?
        # then multiply, but also to dac to fft to out

        num_paths = 0
        for i, requirement in enumerate(requirements):
            paths = self.find_paths(start, requirement)
            for j in range(i + 1, len(requirements)):
                next_segment = self.find_paths(requirement, requirements[j])
                last_segment = self.find_paths(requirements[j], end)
                num_paths += paths * next_segment * last_segment

        return num_paths


class NetworkParser:

    @staticmethod
    def parse(junctions: str) -> Network:
        vertices: List[str] = []
        edges: Dict[int, List[str]] = dict()
        for line in junctions.splitlines():
            if not line.strip():
                continue

            vertices.append(line[:3])

            edges[len(vertices) - 1] = [
                edge.strip() for edge in line[4:].split(" ") if edge.strip()
            ]

        vertices.append("out")
        graph = Graph(len(vertices))
        for vertex, target in edges.items():
            for t in target:
                if not target:
                    continue

                graph.add_edge(int(vertex), vertices.index(t))

        return Network(vertices, graph)


def run() -> int:

    with open("input.txt", "r") as f:
        network = NetworkParser().parse(f.read())

    return network.find_dac_fft_paths("svr", "out", ["fft", "dac"])


if __name__ == "__main__":
    print(run())
