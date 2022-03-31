/*
#include "algorithms.h"

#include <pybind11/pybind11.h>

#include <limits>
#include <queue>
#include <tuple>
#include <unordered_map>
#include <vector>


std::unordered_map<Square, Square> dijkstra(
    const std::vector<std::vector<Square>>& graph,
    const Square& start,
    const Square& end,
    const Square& ignore_node,
    bool draw_best_path = true,
    bool visualize = true
)
{
    // Used to determine the order of squares to check. Order of args helper decide the priority.
    int queue_pos{ 0 };
    std::tuple<int, int, Square> queue_tuple{ std::make_tuple(0, queue_pos, start) };
    std::priority_queue<std::tuple<int, int, Square>> open_set{}; // May need to specific vector elements and define comparison for square
    open_set.push(queue_tuple);

    // Determine what is the best square to check
    std::unordered_map<Square, int> g_score{};
    for (const auto& row : graph)
    {
        for (const auto& square : row)
        {
            g_score[square] = std::numeric_limits<int>::max();
        }
    }
    g_score[start] = 0;

    // Keeps track of next node for every node in graph. A linked list basically.
    std::unordered_map<Square, Square> came_from{};

    // Continues until every node has been checked or best path found
    int i{ 0 };
    while (!open_set.empty())
    {
        // Gets the square currently being checked
        Square curr_square{ std::get<2>(open_set.top()) };
        curr_square = Square();

        // Terminates if found the best path
        if (curr_square == end)
        {
            if (draw_best_path)
            {
                best_path(came_from, end, visualize);
            }
            return came_from;
        }

        // Decides the order of neighbours to check
        for (const auto& nei : curr_square.get_neighbours())
        {
            int temp_g_score{ g_score[curr_square] + 1 };
            if (temp_g_score < g_score[nei])
            {
                came_from[nei] = curr_square;
                g_score[nei] = temp_g_score;

                ++queue_pos;
                std::tuple<int, int, Square> queue_tuple{ std::make_tuple(g_score[nei], queue_pos, nei) };
                open_set.push(queue_tuple);
                if (nei != end && !nei.is_closed() && nei != ignore_node)
                    nei.set_open();
            }
        }

        // Sets square to closed after finished checking
        bool already_closed{ curr_square.is_closed() };
        if (curr_square != start && curr_square != ignore_node)
            curr_square.set_closed();
    }
    return came_from;
}


namespace py = pybind11;

PYBIND11_MODULE(pathfinding_cpp_algorithms, m) {
    m.def("dijkstra", &dijkstra);
    m.def("a_star", &a_star);
    m.def("bi_dijkstra", &bi_dijkstra);

#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif
}
*/