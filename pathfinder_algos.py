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