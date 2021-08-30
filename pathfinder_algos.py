import heapq
import operator
from warnings import warn
from graph import Graph, Vertex, Node


# Use Jeff's city data as SQL database, allow to pick from any city to another
# Go from point A, to B, and then C
# Walls
# Random mazes
# Random shapes

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


def bellman_ford(maze, start):
    for current_vertex in maze.adjacency_list:
        current_vertex.distance = float('inf')
        current_vertex.pred_vertex = None

    start.distance = 0

    for i in range(len(maze.adjacency_list) - 1):
        for current_vertex in maze.adjacency_list:
            for adj_vertex in maze.adjacency_list[current_vertex]:
                edge_weight = maze.edge_weights[(current_vertex, adj_vertex)]
                alternative_path_distance = current_vertex.distance + edge_weight

                if alternative_path_distance < adj_vertex.distance:
                    adj_vertex.distance = alternative_path_distance
                    adj_vertex.pred_vertex = current_vertex

    for current_vertex in maze.adjacency_list:
        for adj_vertex in maze.adjacency_list[current_vertex]:
            edge_weight = maze.edge_weights[(current_vertex, adj_vertex)]
            alternative_path_distance = current_vertex.distance + edge_weight

            if alternative_path_distance < adj_vertex.distance:
                return False

    return True


def dijkstra(maze, start):
    unvisited_queue = []
    for current_vertex in maze.adjacency_list:
        unvisited_queue.append(current_vertex)

    start.distance = 0

    while len(unvisited_queue) > 0:

        smallest_index = 0
        for i in range(1, len(unvisited_queue)):
            if unvisited_queue[i].distance < unvisited_queue[smallest_index].distance:
                smallest_index = i
        current_vertex = unvisited_queue.pop(smallest_index)

        for adj_vertex in maze.adjacency_list[current_vertex]:
            edge_weight = maze.edge_weights[(current_vertex, adj_vertex)]
            alternative_path_distance = current_vertex.distance + edge_weight

            if alternative_path_distance < adj_vertex.distance:
                adj_vertex.distance = alternative_path_distance
                adj_vertex.pred_vertex = current_vertex


# Make own a_star from scratch using graph.py
# def _a_star(graph, start, stop):
#     open_lst = {[start]}
#     closed_lst = set([])
#
#     poo = {start: 0}
#     par = {start: start}
#
#     while len(open_lst) > 0:
#         n = None
#
#         for v in open_lst:
#             if n is None or poo[v] + h(v) < poo[n] + h(n):
#                 n = v
#
#         if n is None:
#             print('Path does not exist!')
#             return None
#
#         if n == stop:
#             reconst_path = []
#
#             while par[n] != n:
#                 reconst_path.append(n)
#                 n = par[n]
#
#             reconst_path.append(start)
#
#             reconst_path.reverse()
#
#             print('Path found: {}'.format(reconst_path))
#             return reconst_path
#
#         for (m, weight) in graph.get_neighbors(n):
#             if m not in open_lst and m not in closed_lst:
#                 open_lst.add(m)
#                 par[m] = n
#                 poo[m] = poo[n] + weight
#
#             else:
#                 if poo[m] > poo[n] + weight:
#                     poo[m] = poo[n] + weight
#                     par[m] = n
#
#                     if m in closed_lst:
#                         closed_lst.remove(m)
#                         open_lst.add(m)
#
#         open_lst.remove(n)
#         closed_lst.add(n)
#
#     print('Path does not exist!')
#     return None


def a_star(maze, start, end, allow_diagonal_movement=False):
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    open_list = []
    closed_list = []

    heapq.heapify(open_list)
    heapq.heappush(open_list, start_node)

    # Adding a stop condition
    outer_iterations = 0
    max_iterations = (len(maze[0]) * len(maze) // 2)

    # what squares do we search
    adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0),)
    if allow_diagonal_movement:
        adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1),)

    # Loop until you find the end
    while len(open_list) > 0:
        outer_iterations += 1

        if outer_iterations > max_iterations:
            # if we hit this point return the path such as it is
            # it will not contain the destination
            warn("giving up on pathfinding too many iterations")
            return return_path(current_node)

            # Get the current node
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            return return_path(current_node)

        # Generate children
        children = []

        for new_position in adjacent_squares:  # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                    len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
            # Child is on the closed list
            if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                        (child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            if len([open_node for open_node in open_list if
                    child.position == open_node.position and child.g > open_node.g]) > 0:
                continue

            # Add the child to the open list
            heapq.heappush(open_list, child)

    warn("Couldn't get a path to destination")
    return None


def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1]  # Return reversed path
