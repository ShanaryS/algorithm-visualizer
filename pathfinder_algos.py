import operator
from graph import Graph, Vertex


# Use Jeff's city data as SQL database, allow to pick from any city to another
# Go from point A, to B, and then C
# test (main)

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


def a_star():
    pass


def get_shortest_path(graph, start_vertex, end_vertex):
    path = ""
    current_vertex = end_vertex
    distance = 0.0
    while current_vertex is not start_vertex:
        if current_vertex is None:
            return "No path"
        path = " -> " + str(current_vertex.label) + path
        if current_vertex.pred_vertex is not None:
            distance += graph.edge_weights[(current_vertex.pred_vertex, current_vertex)]
        current_vertex = current_vertex.pred_vertex
    path = start_vertex.label + path + " (%g)" % distance
    return path
