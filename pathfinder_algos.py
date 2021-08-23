import operator
from graph import Graph, Vertex


# Use Jeff's city data as SQL database, allow to pick from any city to another
# Go from point A, to B, and then C


def bellman_ford(graph, start):
    for current_vertex in graph.adjacency_list:
        current_vertex.distance = float('inf')
        current_vertex.pred_vertex = None

    start.distance = 0

    for i in range(len(graph.adjacency_list) - 1):
        for current_vertex in graph.adjacency_list:
            for adj_vertex in graph.adjacency_list[current_vertex]:
                edge_weight = graph.edge_weights[(current_vertex, adj_vertex)]
                alternative_path_distance = current_vertex.distance + edge_weight

                if alternative_path_distance < adj_vertex.distance:
                    adj_vertex.distance = alternative_path_distance
                    adj_vertex.pred_vertex = current_vertex

    for current_vertex in graph.adjacency_list:
        for adj_vertex in graph.adjacency_list[current_vertex]:
            edge_weight = graph.edge_weights[(current_vertex, adj_vertex)]
            alternative_path_distance = current_vertex.distance + edge_weight

            if alternative_path_distance < adj_vertex.distance:
                return False

    return True


def dijkstra(graph, start):
    unvisited_queue = []
    for current_vertex in graph.adjacency_list:
        unvisited_queue.append(current_vertex)

    start.distance = 0

    while len(unvisited_queue) > 0:

        smallest_index = 0
        for i in range(1, len(unvisited_queue)):
            if unvisited_queue[i].distance < unvisited_queue[smallest_index].distance:
                smallest_index = i
        current_vertex = unvisited_queue.pop(smallest_index)

        for adj_vertex in graph.adjacency_list[current_vertex]:
            edge_weight = graph.edge_weights[(current_vertex, adj_vertex)]
            alternative_path_distance = current_vertex.distance + edge_weight

            if alternative_path_distance < adj_vertex.distance:
                adj_vertex.distance = alternative_path_distance
                adj_vertex.pred_vertex = current_vertex


def a_star(): #TODO
    pass


def get_shortest_path(graph, start, end_vertex):
    trail = ""
    current_vertex = end_vertex
    distance = 0.0
    while current_vertex is not start:
        if current_vertex is None:
            return "No path"
        trail = " -> " + str(current_vertex.label) + trail
        if current_vertex.pred_vertex is not None:
            distance += graph.edge_weights[(current_vertex.pred_vertex, current_vertex)]
        current_vertex = current_vertex.pred_vertex
    trail = start.label + trail + " (%g)" % distance
    return trail


if __name__ == "__main__":
    # Bellman ford test
    b = Graph()

    vertex_A = Vertex("A")
    vertex_B = Vertex("B")
    vertex_C = Vertex("C")
    vertex_D = Vertex("D")
    vertex_E = Vertex("E")
    vertex_F = Vertex("F")

    b.add_vertex(vertex_A)
    b.add_vertex(vertex_B)
    b.add_vertex(vertex_C)
    b.add_vertex(vertex_D)
    b.add_vertex(vertex_E)
    b.add_vertex(vertex_F)

    b.add_directed_edge(vertex_A, vertex_B, 1)
    b.add_directed_edge(vertex_A, vertex_C, 2)
    b.add_undirected_edge(vertex_B, vertex_C, 1)
    b.add_undirected_edge(vertex_B, vertex_D, 3)
    b.add_directed_edge(vertex_B, vertex_E, 2)
    b.add_undirected_edge(vertex_C, vertex_E, 2)
    b.add_directed_edge(vertex_D, vertex_C, 1)
    b.add_undirected_edge(vertex_D, vertex_E, 4)
    b.add_directed_edge(vertex_D, vertex_F, 3)
    b.add_directed_edge(vertex_E, vertex_F, 3)

    start_vertex = vertex_A
    bellman_ford_test = b

    if bellman_ford(bellman_ford_test, start_vertex):
        for v in bellman_ford_test.adjacency_list:
            path = get_shortest_path(bellman_ford_test, start_vertex, v)
            print(f"{start_vertex.label} -> {v.label}: {path}")
    else:
        print("Bellman-Ford failed, negative edge weight cycle detected.")

    print("----------------------------------------------------------------")

    # Dijkstra test
    d = Graph()

    vertex_a = Vertex("A")
    vertex_b = Vertex("B")
    vertex_c = Vertex("C")
    vertex_d = Vertex("D")
    vertex_e = Vertex("E")
    vertex_f = Vertex("F")
    vertex_g = Vertex("G")

    d.add_vertex(vertex_a)
    d.add_vertex(vertex_b)
    d.add_vertex(vertex_c)
    d.add_vertex(vertex_d)
    d.add_vertex(vertex_e)
    d.add_vertex(vertex_f)
    d.add_vertex(vertex_g)

    d.add_undirected_edge(vertex_a, vertex_b, 8)
    d.add_undirected_edge(vertex_a, vertex_c, 7)
    d.add_undirected_edge(vertex_a, vertex_d, 3)
    d.add_undirected_edge(vertex_b, vertex_e, 6)
    d.add_undirected_edge(vertex_c, vertex_d, 1)
    d.add_undirected_edge(vertex_c, vertex_e, 2)
    d.add_undirected_edge(vertex_d, vertex_f, 15)
    d.add_undirected_edge(vertex_d, vertex_g, 12)
    d.add_undirected_edge(vertex_e, vertex_f, 4)
    d.add_undirected_edge(vertex_f, vertex_g, 1)

    dijkstra_test = d
    dijkstra(dijkstra_test, vertex_a)

    for v in sorted(dijkstra_test.adjacency_list, key=operator.attrgetter("label")):
        if v.pred_vertex is None and v is not vertex_a:
            print(f"A to {v.label}: no path exists")
        else:
            print(f"A to {v.label}: {get_shortest_path(dijkstra_test, vertex_a, v)}")

    print("----------------------------------------------------------------")