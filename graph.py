class Vertex:
    def __init__(self, label):
        self.label = label
        self.distance = float('inf')
        self.pred_vertex = None


class Graph:
    def __init__(self):
        self.adjacency_list = {}
        self.edge_weights = {}

    def get_neighbors(self, v):
        return self.adjacency_list[v]

    def add_vertex(self, new_vertex):
        self.adjacency_list[new_vertex] = []

    def add_directed_edge(self, from_vertex, to_vertex, weight=1.0):
        self.edge_weights[(from_vertex, to_vertex)] = weight
        self.adjacency_list[from_vertex].append(to_vertex)

    def add_undirected_edge(self, vertex_a, vertex_b, weight=1.0):
        self.add_directed_edge(vertex_a, vertex_b, weight)
        self.add_directed_edge(vertex_b, vertex_a, weight)


class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __repr__(self):
        return f"{self.position} - g: {self.g} h: {self.h} f: {self.f}"

    def __lt__(self, other):
        return self.f < other.f

    def __gt__(self, other):
        return self.f > other.f


def heuristic(n):
    h = {
        'A': 1,
        'B': 1,
        'C': 1,
        'D': 1
    }

    return h[n]