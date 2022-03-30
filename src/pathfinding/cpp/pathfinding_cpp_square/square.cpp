#include <pybind11/pybind11.h>

#include "square.h"


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