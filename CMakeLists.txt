cmake_minimum_required(VERSION 3.0.0)

project(AlgorithmVisualizer)

set(CMAKE_CXX_STANDARD 20)

set(pybind11_DIR ${CMAKE_SOURCE_DIR}/venv/Lib/site-packages/pybind11/share/cmake/pybind11)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/src/pathfinding/cpp)

find_package(pybind11 CONFIG)
pybind11_add_module(square ${CMAKE_SOURCE_DIR}/src/pathfinding/cpp/square.cpp)
pybind11_add_module(algorithms ${CMAKE_SOURCE_DIR}/src/pathfinding/cpp/algorithms.cpp)