cmake_minimum_required(VERSION 3.0.0)

project(AlgorithmVisualizer)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/src/pathfinding/cpp)

add_subdirectory(thirdparty/pybind11)
pybind11_add_module(square src/pathfinding/cpp/square.cpp)
pybind11_add_module(algorithms src/pathfinding/cpp/algorithms.cpp)