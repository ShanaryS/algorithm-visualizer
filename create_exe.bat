set name="Pathfinding Visualizer"

venv\Scripts\pyinstaller.exe -F -n %name% --distpath ./bin -p "venv\Lib\site-packages" --noconsole run_pathfinding_visualizer.py

del %name%".spec"
rmdir /s /q "__pycache__" "build"

set name="Sorting Visualizer"

venv\Scripts\pyinstaller.exe -F -n %name% --distpath ./bin -p "venv\Lib\site-packages" --noconsole run_sort_visualizer.py

del %name%".spec"
rmdir /s /q "__pycache__" "build"

set name="Searching Visualizer"

venv\Scripts\pyinstaller.exe -F -n %name% --distpath ./bin -p "venv\Lib\site-packages" --noconsole run_search_visualizer.py

del %name%".spec"
rmdir /s /q "__pycache__" "build"
