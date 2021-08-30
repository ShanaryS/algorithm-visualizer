from vis import SearchVisualizer, SortVisualizer, PathfindingVisualizer
from pathfinder_algos import bellman_ford, dijkstra, a_star, get_shortest_path
from graph import Graph, Vertex
import operator

if __name__ == '__main__':
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


    def example(print_maze=True):

        maze = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ] * 2,
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ] * 2,
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ] * 2,
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ] * 2,
                [0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, ] * 2,
                [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, ] * 2,
                [0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, ] * 2,
                [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, ] * 2,
                [0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, ] * 2,
                [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, ] * 2,
                [0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, ] * 2,
                [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, ] * 2,
                [0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, ] * 2,
                [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, ] * 2,
                [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, ] * 2,
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, ] * 2, ]

        start = (0, 0)
        end = (len(maze) - 1, len(maze[0]) - 1)

        path = a_star(maze, start, end)

        if print_maze:
            for step in path:
                maze[step[0]][step[1]] = 2

            for row in maze:
                line = []
                for col in row:
                    if col == 1:
                        line.append("\u2588")
                    elif col == 0:
                        line.append(" ")
                    elif col == 2:
                        line.append(".")
                print("".join(line))

        print(path)

    example()

    # ------------------------------------------------------------------------------
    # A* test

    # a_star(d, 'A', 'D')

    # adjac_lis = {
    #     'A': [('B', 1), ('C', 3), ('D', 7)],
    #     'B': [('D', 5)],
    #     'C': [('D', 12)]
    # }
    # graph1 = Graph(adjac_lis)
    # graph1.a_star_algorithm('A', 'D')

    # -----------------------------------------------------------------------------
    # -----------------------------------------------------------------------------
    # -----------------------------------------------------------------------------
    # -----------------------------------------------------------------------------
    # -----------------------------------------------------------------------------
    # -----------------------------------------------------------------------------

    # Search = SearchVisualizer()
    # Sort = SortVisualizer()
    # # Search.set_graph()
    # Sort.set_graph()

    # Below was to test without GUI. No longer need doesn't harm to keep
    # test = [4, 89, 1, 9, 69, 49, 149, 84, 15, 15, 79, 41, 9, 62, 19]  # Original test array. Use as base. 48/49
    # test1 = [4, 89, 1, 9, 69, 49, 149, 84, 15, 79, 41, 62, 19]  # No duplicates
    # test2 = [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
    #
    # size = 100  # Range from 5 to 100
    # test3 = np.random.randint(0, 150, size)
    #
    # values = test3
    # # Sort = SortVisualizer(values)
    # # Sort.set_graph()
    #
    # # Sort.merge()
    # # Sort.radix()
    # # Sort.quick()
    # # Sort.heap()
    # # Sort.tim()
    #
    # # Sort.insertion()
    # # Sort.selection()
    # # Sort.bubble()
    #
    # # Sort.bogo()
    #
    # # ---------------------------------------------------------
    # Search = SearchVisualizer(values)
    # Search.set_graph()
    # key = 83
    #
    # # Search.binary(key)
    # # Search.jump(key)
    # # Search.exponential(key)
    # # Search.fibonacci(key)
    # # Search.linear(key)
    # # Search.comparison(key)



