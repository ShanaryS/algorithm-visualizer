@echo off

rmdir /s /q "bin"

set name="Pathfinding Visualizer"
set src="run_pathfinding_visualizer.py"

venv\Scripts\pyinstaller.exe -F -n %name% -p "venv\Lib\site-packages" -p "src\pathfinding" --noconsole --distpath ./bin %src%
signtool sign /a bin\\%name%.exe
signtool timestamp /t http://timestamp.digicert.com bin\\%name%.exe

del %name%".spec"
rmdir /s /q "__pycache__" "build"
mkdir "bin\lib"
copy "lib\.env" "bin\lib"
copy "lib\include_cpp.json" "bin\lib"
copy "venv\Lib\site-packages\certifi\cacert.pem" "bin\lib"


set name="Sorting Visualizer"
set src="run_sorting_visualizer.py"

venv\Scripts\pyinstaller.exe -F -n %name% -p "venv\Lib\site-packages" -p "src\sorting" --noconsole --distpath ./bin %src%
signtool sign /a bin\\%name%.exe
signtool timestamp /t http://timestamp.digicert.com bin\\%name%.exe

del %name%".spec"
rmdir /s /q "__pycache__" "build"


set name="Searching Visualizer"
set src="run_searching_visualizer.py"

venv\Scripts\pyinstaller.exe -F -n %name% -p "venv\Lib\site-packages" -p "src\searching" --noconsole --distpath ./bin %src%
signtool sign /a bin\\%name%.exe
signtool timestamp /t http://timestamp.digicert.com bin\\%name%.exe

del %name%".spec"
rmdir /s /q "__pycache__" "build"


echo.
echo --------------------------------------------------------------
echo Executable located in "bin" directory.
echo.
pause
