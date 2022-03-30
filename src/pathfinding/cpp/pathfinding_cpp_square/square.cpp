#include <pybind11/pybind11.h>

#include "square.h"


std::vector<Square> Square::get_neighbours(bool include_walls = false) const
{
    std::vector<Square> neighbours;
    for (std::pair<const std::string&, Square> direction : m_neighbours)
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

void Square::reset(){}

void Square::set_open(){}

void Square::set_open2(){}

void Square::set_open3(){}

void Square::set_closed(){}

void Square::set_closed2(){}

void Square::set_closed3(){}

void Square::set_start(){}

void Square::set_mid(){}

void Square::set_end(){}

void Square::set_wall(){}

void Square::set_path(){}

void Square::set_history(){}

void Square::update_neighbours(auto gph){}

void Square::s_clear_all_node_lists(){}

void Square::discard_node(bool remove_wall = true){}

// Allow code to be imported into python using pybind11

namespace py = pybind11;

PYBIND11_MODULE(pathfinding_cpp_node, m) {
    py::class_<Square>(m, "Square")
        .def("reset", &Square::reset);

#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif
}