#include <pybind11/pybind11.h>
#include <iostream>

void my_func()
{
    std::cout << "It's working!\n";
}

namespace py = pybind11;

PYBIND11_MODULE(pathfinding_cpp_node, m) {
    m.def("my_func", &my_func, R"pbdoc(
        Amazing!
    )pbdoc");

#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif
}