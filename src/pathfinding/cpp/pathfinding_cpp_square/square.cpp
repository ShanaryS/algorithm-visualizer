#include <pybind11/pybind11.h>

#include "square.h"


std::array<Square, 4> get_neighbours(bool include_walls = false) const;
std::tuple<std::array<int, 3>, std::tuple<float, int>> draw_square() const;


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