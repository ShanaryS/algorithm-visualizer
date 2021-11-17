@echo off

set name="Pathfinding Visualizer"
set src="run_pathfinding_visualizer.py"

venv\Scripts\pyinstaller.exe -F -n %name% --distpath ./bin -p "venv\Lib\site-packages" --noconsole %src%

del %name%".spec"
rmdir /s /q "__pycache__" "build"


set name="Sorting Visualizer"
set src="run_sort_visualizer.py"

venv\Scripts\pyinstaller.exe -F -n %name% --distpath ./bin -p "venv\Lib\site-packages" --noconsole %src%

del %name%".spec"
rmdir /s /q "__pycache__" "build"


set name="Searching Visualizer"
set src="run_search_visualizer.py"

venv\Scripts\pyinstaller.exe -F -n %name% --distpath ./bin -p "venv\Lib\site-packages" --noconsole %src%

del %name%".spec"
rmdir /s /q "__pycache__" "build"


echo.
echo --------------------------------------------------------------
echo Executable and source files located in "bin" directory.
echo.
pause
