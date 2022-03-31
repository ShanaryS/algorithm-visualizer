"""Package for sorting visualizer"""


"""import sys
from src.package_paths import package_paths


# This allows less verbose importing (e.g py.algorithms)
curr_package = "sorting"
if package_paths[curr_package] not in sys.path:
    sys.path.append(package_paths[curr_package])

# Prevent running two visualizers at the same time as module names are similar.
other_packages = package_paths.copy()  # To prevent changing actual variable
other_packages.pop(curr_package)
for package in other_packages:
    if package in sys.path:
        raise ImportError("Cannot run two visualizers at the same time.")"""
