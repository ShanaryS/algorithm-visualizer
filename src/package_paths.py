"""Place to add package paths to sys.path in each packages' __init__.py."""


import os


package_paths = {
    "pathfinding": os.path.join("src", "pathfinding"),
    "sorting": os.path.join("src", "sorting"),
    "searching": os.path.join("src", "searching")
}