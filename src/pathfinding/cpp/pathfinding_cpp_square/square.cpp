#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/operators.h>

#include "square.h"


std::vector<Square> Square::get_neighbours(bool include_walls) const
{
    std::vector<Square> neighbours;
    for (const auto& direction : m_neighbours)
    {
        Square nei{ direction.second };
        if (static_cast<bool>(nei))
        {
            if (!nei.is_wall())
            {
                neighbours.push_back(nei);
            }
            else if (include_walls)
            {
                neighbours.push_back(nei);
            }
        }
    }
    return neighbours;
}

std::tuple<std::array<int, 3>, std::tuple<float, float, int, int>> Square::draw_square() const
{
    auto square_pos = std::make_tuple(m_x, m_y, static_cast<int>(m_square_size), static_cast<int>(m_square_size));
    return std::make_tuple(m_color, square_pos);
}

void Square::reset()
{
    // Don't do anything if already set correctly
    if (is_empty()) { return; }

    // Add to note history if user requests to track
    if (s_track_node_history)
    {
        s_node_history.insert(*this);
    }

    discard_node();
    m_color = s_default_color;
    m_is_highway = false;
    s_nodes_to_update.insert(*this);
    s_all_empty_nodes.insert(*this);
}

void Square::set_open()
{
    // Don't do anything if already set correctly
    if (is_open()) { return; }

    // Add to note history if user requests to track
    if (s_track_node_history)
    {
        s_node_history.insert(*this);
    }

    discard_node();
    m_color = s_open_color;
    s_nodes_to_update.insert(*this);
    s_all_open_nodes.insert(*this);
}

void Square::set_open2()
{
    // Don't do anything if already set correctly
    if (is_open2()) { return; }

    // Add to note history if user requests to track
    if (s_track_node_history)
    {
        s_node_history.insert(*this);
    }

    discard_node();
    m_color = s_open2_color;
    s_nodes_to_update.insert(*this);
    s_all_open2_nodes.insert(*this);
}

void Square::set_open3()
{
    // Don't do anything if already set correctly
    if (is_open3()) { return; }

    // Add to note history if user requests to track
    if (s_track_node_history)
    {
        s_node_history.insert(*this);
    }

    discard_node();
    m_color = s_open3_color;
    s_nodes_to_update.insert(*this);
    s_all_open3_nodes.insert(*this);
}

void Square::set_closed()
{
    // Don't do anything if already set correctly
    if (is_closed()) { return; }

    // Add to note history if user requests to track
    if (s_track_node_history)
    {
        s_node_history.insert(*this);
    }

    discard_node();
    m_color = s_closed_color;
    s_nodes_to_update.insert(*this);
    s_all_closed_nodes.insert(*this);
}

void Square::set_closed2()
{
    // Don't do anything if already set correctly
    if (is_closed2()) { return; }

    // Add to note history if user requests to track
    if (s_track_node_history)
    {
        s_node_history.insert(*this);
    }

    discard_node();
    m_color = s_closed2_color;
    s_nodes_to_update.insert(*this);
    s_all_closed2_nodes.insert(*this);
}

void Square::set_closed3()
{
    // Don't do anything if already set correctly
    if (is_closed3()) { return; }

    // Add to note history if user requests to track
    if (s_track_node_history)
    {
        s_node_history.insert(*this);
    }

    discard_node();
    m_color = s_closed3_color;
    s_nodes_to_update.insert(*this);
    s_all_closed3_nodes.insert(*this);
}

void Square::set_start()
{
    // Don't do anything if already set correctly
    if (is_start()) { return; }

    // Add to note history if user requests to track
    if (s_track_node_history)
    {
        s_node_history.insert(*this);
    }

    discard_node(false);  // Don't remove ordinal node
    m_color = s_start_color;
    s_nodes_to_update.insert(*this);
    s_all_start_nodes.insert(*this);
}

void Square::set_mid()
{
    // Don't do anything if already set correctly
    if (is_mid()) { return; }

    // Add to note history if user requests to track
    if (s_track_node_history)
    {
        s_node_history.insert(*this);
    }

    discard_node(false);  // Don't remove ordinal node
    m_color = s_mid_color;
    s_nodes_to_update.insert(*this);
    s_all_mid_nodes.insert(*this);
}

void Square::set_end()
{
    // Don't do anything if already set correctly
    if (is_end()) { return; }

    // Add to note history if user requests to track
    if (s_track_node_history)
    {
        s_node_history.insert(*this);
    }

    discard_node(false);  // Don't remove ordinal node
    m_color = s_end_color;
    s_nodes_to_update.insert(*this);
    s_all_end_nodes.insert(*this);
}

void Square::set_wall()
{
    // Don't do anything if already set correctly
    if (is_wall()) { return; }

    // Add to note history if user requests to track
    if (s_track_node_history)
    {
        s_node_history.insert(*this);
    }

    discard_node();
    m_color = m_wall_color;
    s_nodes_to_update.insert(*this);
    s_all_wall_nodes.insert(*this);
}

void Square::set_path()
{
    // Don't do anything if already set correctly
    if (is_path()) { return; }

    // Add to note history if user requests to track
    if (s_track_node_history)
    {
        s_node_history.insert(*this);
    }

    discard_node();
    m_color = s_path_color;
    s_nodes_to_update.insert(*this);
    s_all_path_nodes.insert(*this);
}

void Square::set_history()
{
    // Don't do anything if already set correctly
    if (is_history()) { return; }

    // Add to note history if user requests to track
    if (is_path() || is_start() || is_mid() || is_end())
    {
        s_node_history.insert(*this);
    }

    // Don't discard node from list as will be immediately revert color
    // Also don't add to nodes_to_update as it is handled differently
    m_color_history = m_color;
    m_color = s_history_color;
    s_all_history_nodes.insert(*this);
}

void Square::s_update_neighbours(std::vector<std::vector<Square>>& graph)
{
    for (auto& row : graph)
    {
        for (auto& square : row)
        {
            square.update_neighbours(graph);
        }
    }
}

void Square::s_clear_all_node_lists()
{
    s_all_empty_nodes.clear();
    s_all_open_nodes.clear();
    s_all_open2_nodes.clear();
    s_all_open3_nodes.clear();
    s_all_closed_nodes.clear();
    s_all_closed2_nodes.clear();
    s_all_closed3_nodes.clear();
    s_all_start_nodes.clear();
    s_all_mid_nodes.clear();
    s_all_end_nodes.clear();
    s_all_wall_nodes.clear();
    s_all_path_nodes.clear();
    s_all_history_nodes.clear();
}

void Square::update_neighbours(std::vector<std::vector<Square>>& graph)
{
    if (m_col > 0) { m_neighbours.insert({ "Left", graph[m_row][m_col - 1] }); }
    if (m_row > 0) { m_neighbours.insert({ "Up", graph[m_row - 1][m_col] }); }
    if (m_col < m_rows - 1) { m_neighbours.insert({ "Right", graph[m_row][m_col + 1] }); }
    if (m_row < m_rows - 1) { m_neighbours.insert({ "Down", graph[m_row + 1][m_col] }); }
}

void Square::discard_node(bool remove_wall)
{
    // Ordinal nodes should not remove wall to reinstate after dragging
    if (!remove_wall && m_color == m_wall_color) { return; }
    
    // Remove this squares color from corresponding list
    if (m_color == s_default_color) { s_all_empty_nodes.erase(*this); }
    else if (m_color == s_open_color) { s_all_open_nodes.erase(*this); }
    else if (m_color == s_open2_color) { s_all_open2_nodes.erase(*this); }
    else if (m_color == s_open3_color) { s_all_open3_nodes.erase(*this); }
    else if (m_color == s_closed_color) { s_all_closed_nodes.erase(*this); }
    else if (m_color == s_closed2_color) { s_all_closed2_nodes.erase(*this); }
    else if (m_color == s_closed3_color) { s_all_closed3_nodes.erase(*this); }
    else if (m_color == s_start_color) { s_all_start_nodes.erase(*this); }
    else if (m_color == s_mid_color) { s_all_mid_nodes.erase(*this); }
    else if (m_color == s_end_color) { s_all_end_nodes.erase(*this); }
    else if (m_color == m_wall_color) { s_all_wall_nodes.erase(*this); }
    else if (m_color == s_path_color) { s_all_path_nodes.erase(*this); }
    else if (m_color == s_history_color) { s_all_history_nodes.erase(*this); }
}

// Allow code to be imported into python using pybind11

namespace py = pybind11;

PYBIND11_MODULE(pathfinding_cpp_square, m) {
    py::class_<Square>(m, "Square")
        .def(py::init<int, int, int, float>())
        .def(py::self == py::self)
        .def(py::self != py::self)
        .def("get_pos", &Square::get_pos)
        .def("get_color", &Square::get_color)
        .def("get_neighbours", &Square::get_neighbours)
        .def("draw_square", &Square::draw_square)
        .def("is_empty", &Square::is_empty)
        .def("is_open", &Square::is_open)
        .def("is_open2", &Square::is_open2)
        .def("is_open3", &Square::is_open3)
        .def("is_closed", &Square::is_closed)
        .def("is_closed2", &Square::is_closed2)
        .def("is_closed3", &Square::is_closed3)
        .def("is_start", &Square::is_start)
        .def("is_mid", &Square::is_mid)
        .def("is_end", &Square::is_end)
        .def("is_wall", &Square::is_wall)
        .def("is_path", &Square::is_path)
        .def("is_history", &Square::is_history)
        .def("reset", &Square::reset)
        .def("set_open", &Square::set_open)
        .def("set_open2", &Square::set_open2)
        .def("set_open3", &Square::set_open3)
        .def("set_closed", &Square::set_closed)
        .def("set_closed2", &Square::set_closed2)
        .def("set_closed3", &Square::set_closed3)
        .def("set_start", &Square::set_start)
        .def("set_mid", &Square::set_mid)
        .def("set_end", &Square::set_end)
        .def("set_wall", &Square::set_wall)
        .def("set_path", &Square::set_path)
        .def("set_history", &Square::set_history)
        .def("set_history_rollback", &Square::set_history_rollback)
        .def("update_neighbours", &Square::s_update_neighbours)
        .def("reset_wall_color", &Square::reset_wall_color)
        .def("set_wall_color_map", &Square::set_wall_color_map)
        .def("get_all_empty_nodes", &Square::s_get_all_empty_nodes)
        .def("get_all_open_nodes", &Square::s_get_all_open_nodes)
        .def("get_all_open2_nodes", &Square::s_get_all_open2_nodes)
        .def("get_all_open3_nodes", &Square::s_get_all_open3_nodes)
        .def("get_all_closed_nodes", &Square::s_get_all_closed_nodes)
        .def("get_all_closed2_nodes", &Square::s_get_all_closed2_nodes)
        .def("get_all_closed3_nodes", &Square::s_get_all_closed3_nodes)
        .def("get_all_start_nodes", &Square::s_get_all_start_nodes)
        .def("get_all_mid_nodes", &Square::s_get_all_mid_nodes)
        .def("get_all_end_nodes", &Square::s_get_all_end_nodes)
        .def("get_all_wall_nodes", &Square::s_get_all_wall_nodes)
        .def("get_all_path_nodes", &Square::s_get_all_path_nodes)
        .def("get_all_history_nodes", &Square::s_get_all_history_nodes)
        .def("get_nodes_to_update", &Square::s_get_nodes_to_update)
        .def("get_node_history", &Square::s_get_node_history)
        .def("get_track_node_history", &Square::s_get_track_node_history)
        .def("clear_nodes_to_update", &Square::s_clear_nodes_to_update)
        .def("clear_history_nodes", &Square::s_clear_history_nodes)
        .def("clear_node_history", &Square::s_clear_node_history)
        .def("clear_all_node_lists", &Square::s_clear_all_node_lists)
        .def("set_track_node_history", &Square::s_set_track_node_history);

#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif
}