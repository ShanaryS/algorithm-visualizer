#include "square.h"

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/operators.h>

#include <stdexcept>


std::vector<std::vector<Square>> Square::init(int rows, int cols, float square_size)
{
    // Reset class
    Square::s_clear_all_node_lists();
    Square::graph = {};

    // Create each square
    for (int row{ 0 }; row < rows; ++row)
    {
        Square::graph.push_back({});
        for (int col{ 0 }; col < cols; ++col)
        {
            Square(row, col, rows, square_size);
        }
    }

    // Return a copy for outside the class
    return Square::graph;
}


// Allow hashing using row and col position
template<>
struct std::hash<Square>
{
    size_t operator()(const Square& square) const
    {
        std::array<int, 2> pos = square.get_pos();
        std::size_t row_hash = std::hash<int>()(pos[0]);
        std::size_t col_hash = std::hash<int>()(pos[1]) << 1;
        return row_hash ^ col_hash;
    }
};

std::vector<Square> Square::get_neighbours(bool include_walls) const
{
    std::vector<Square> neighbours;
    if (m_col > 0)
    { 
        Square& nei = Square::graph[m_row][m_col - 1];
        if (!nei.is_wall()) 
        {
            neighbours.push_back(nei);
        }
        else if (include_walls)
        {
            neighbours.push_back(nei);
        }
    }
    if (m_row > 0)
    {
        Square& nei = Square::graph[m_row - 1][m_col];
        if (!nei.is_wall())
        {
            neighbours.push_back(nei);
        }
        else if (include_walls)
        {
            neighbours.push_back(nei);
        }
    }
    if (m_col < m_rows - 1)
    {
        Square& nei = Square::graph[m_row][m_col + 1];
        if (!nei.is_wall())
        {
            neighbours.push_back(nei);
        }
        else if (include_walls)
        {
            neighbours.push_back(nei);
        }
    }
    if (m_row < m_rows - 1)
    {
        Square& nei = Square::graph[m_row + 1][m_col];
        if (!nei.is_wall())
        {
            neighbours.push_back(nei);
        }
        else if (include_walls)
        {
            neighbours.push_back(nei);
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

// Prevent copies being made when passing these types around
PYBIND11_MAKE_OPAQUE(std::unordered_set<Square, Square::hash>);

namespace py = pybind11;
using namespace pybind11::literals;

PYBIND11_MODULE(pathfinding_cpp_square, m) {
    // Define Python API for opaque types
    py::class_<std::unordered_set<Square, Square::hash>>(m, "unordered_set_square")
        .def(py::init<>())
        .def("copy", [](std::unordered_set<Square, Square::hash>& self) { throw std::runtime_error("Use the copy module in python to copy."); })
        .def("__len__", [](const std::unordered_set<Square, Square::hash>& self) { return self.size(); })
        .def("__iter__", [](std::unordered_set<Square, Square::hash>& self) { return py::make_iterator(self.begin(), self.end()); }, py::keep_alive<0, 1>());

    // Define Python API for Square class
    py::class_<Square>(m, "Square")
        .def(py::init<int, int, int, float>())
        .def("init", &Square::init, py::return_value_policy::copy)
        .def(py::self == py::self)
        .def(py::self != py::self)
        .def(hash(py::self))
        .def("get_pos", &Square::get_pos, py::return_value_policy::reference)
        .def("get_color", &Square::get_color, py::return_value_policy::reference)
        .def("get_neighbours", &Square::get_neighbours, "include_walls"_a=false, py::return_value_policy::reference)
        .def("draw_square", &Square::draw_square, py::return_value_policy::reference)
        .def("is_empty", &Square::is_empty, py::return_value_policy::reference)
        .def("is_open", &Square::is_open, py::return_value_policy::reference)
        .def("is_open2", &Square::is_open2, py::return_value_policy::reference)
        .def("is_open3", &Square::is_open3, py::return_value_policy::reference)
        .def("is_closed", &Square::is_closed, py::return_value_policy::reference)
        .def("is_closed2", &Square::is_closed2, py::return_value_policy::reference)
        .def("is_closed3", &Square::is_closed3, py::return_value_policy::reference)
        .def("is_start", &Square::is_start, py::return_value_policy::reference)
        .def("is_mid", &Square::is_mid, py::return_value_policy::reference)
        .def("is_end", &Square::is_end, py::return_value_policy::reference)
        .def("is_wall", &Square::is_wall, py::return_value_policy::reference)
        .def("is_path", &Square::is_path, py::return_value_policy::reference)
        .def("is_history", &Square::is_history, py::return_value_policy::reference)
        .def("reset", &Square::reset, py::return_value_policy::reference)
        .def("set_open", &Square::set_open, py::return_value_policy::reference)
        .def("set_open2", &Square::set_open2, py::return_value_policy::reference)
        .def("set_open3", &Square::set_open3, py::return_value_policy::reference)
        .def("set_closed", &Square::set_closed, py::return_value_policy::reference)
        .def("set_closed2", &Square::set_closed2, py::return_value_policy::reference)
        .def("set_closed3", &Square::set_closed3, py::return_value_policy::reference)
        .def("set_start", &Square::set_start, py::return_value_policy::reference)
        .def("set_mid", &Square::set_mid, py::return_value_policy::reference)
        .def("set_end", &Square::set_end, py::return_value_policy::reference)
        .def("set_wall", &Square::set_wall, py::return_value_policy::reference)
        .def("set_path", &Square::set_path, py::return_value_policy::reference)
        .def("set_history", &Square::set_history, py::return_value_policy::reference)
        .def("set_history_rollback", &Square::set_history_rollback, py::return_value_policy::reference)
        .def("reset_wall_color", &Square::reset_wall_color, py::return_value_policy::reference)
        .def("set_wall_color_map", &Square::set_wall_color_map, py::return_value_policy::reference)
        .def_static("get_all_empty_nodes", &Square::s_get_all_empty_nodes, py::return_value_policy::reference)
        .def_static("get_all_open_nodes", &Square::s_get_all_open_nodes, py::return_value_policy::reference)
        .def_static("get_all_open2_nodes", &Square::s_get_all_open2_nodes, py::return_value_policy::reference)
        .def_static("get_all_open3_nodes", &Square::s_get_all_open3_nodes, py::return_value_policy::reference)
        .def_static("get_all_closed_nodes", &Square::s_get_all_closed_nodes, py::return_value_policy::reference)
        .def_static("get_all_closed2_nodes", &Square::s_get_all_closed2_nodes, py::return_value_policy::reference)
        .def_static("get_all_closed3_nodes", &Square::s_get_all_closed3_nodes, py::return_value_policy::reference)
        .def_static("get_all_start_nodes", &Square::s_get_all_start_nodes, py::return_value_policy::reference)
        .def_static("get_all_mid_nodes", &Square::s_get_all_mid_nodes, py::return_value_policy::reference)
        .def_static("get_all_end_nodes", &Square::s_get_all_end_nodes, py::return_value_policy::reference)
        .def_static("get_all_wall_nodes", &Square::s_get_all_wall_nodes, py::return_value_policy::reference)
        .def_static("get_all_path_nodes", &Square::s_get_all_path_nodes, py::return_value_policy::reference)
        .def_static("get_all_history_nodes", &Square::s_get_all_history_nodes, py::return_value_policy::reference)
        .def_static("get_nodes_to_update", &Square::s_get_nodes_to_update, py::return_value_policy::reference)
        .def_static("get_node_history", &Square::s_get_node_history, py::return_value_policy::reference)
        .def_static("get_track_node_history", &Square::s_get_track_node_history, py::return_value_policy::reference)
        .def_static("clear_nodes_to_update", &Square::s_clear_nodes_to_update, py::return_value_policy::reference)
        .def_static("clear_history_nodes", &Square::s_clear_history_nodes, py::return_value_policy::reference)
        .def_static("clear_node_history", &Square::s_clear_node_history, py::return_value_policy::reference)
        .def_static("clear_all_node_lists", &Square::s_clear_all_node_lists, py::return_value_policy::reference)
        .def_static("set_track_node_history", &Square::s_set_track_node_history, py::return_value_policy::reference);

#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif
}