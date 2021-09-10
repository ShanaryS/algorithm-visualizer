"""Run different visualizers by uncommenting the desired one"""
from search.graph import set_graph as run_search
from sort.graph import set_graph as run_sort
from pathfinding.logic import main as run_pathfinding


if __name__ == '__main__':
    # run_search(initialize=True)
    # run_sort()
    run_pathfinding()
