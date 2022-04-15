# Algorithm Visualizer

This tool visualizes the operations of the most popular pathfinding, sorting, and searching algorithms. Algorithms are written both in C++ and Python with easy comparisons by editing 'include_cpp.json'. GUI and user inputs are always in python. This was implemented using NumPy and Matplotlib for Search and Sort visualizations, and Pygame with google maps API for pathfinding visualizations. All are fully interactive with multithreading support and per pixel screen refreshes. Visualizers can be easily compilied into a single .exe for portability while maintaining configurability with 'include_cpp.json'.

***

<p align="center">
  <strong>Pathfinding Visualizer:</strong>
</p>

<p align="center">
  Able to draw custom walls and drag nodes after algorithm completion:
</p>

<p align="center">
  <img src="https://user-images.githubusercontent.com/86130442/132488928-2ddace80-7be9-404d-903e-ecfe360bbf7f.gif" alt="animated" />
</p>

<p align="center">
  (Algorithms slowed down for illustration purposes)
</p>

***

<p align="center">
  Visit the streets of anywhere in the world! Powered by google maps API:
</p>

<p align="center">
  <img src="https://user-images.githubusercontent.com/86130442/135311945-822a86b2-e09a-480d-bd98-c21d604a2f8f.gif" alt="animated" />
</p>

<p align="center">
  (Algorithms slowed down for illustration purposes)
</p>

Add mid node to layer the search! Able to drag mid node as well:             |  Generate mazes with recursive division animations or instantly:
:-------------------------:|:-------------------------:
![Pathfinding Demo #2](https://user-images.githubusercontent.com/86130442/132563386-554f632d-e1bf-41f8-9e5d-1f6e06487186.gif)  |  ![Pathfinding Demo #3](https://user-images.githubusercontent.com/86130442/132563681-c7387b5b-f8b3-4e7b-9578-34428a0f850c.gif)

***

<p align="center">
  <strong>Sorting Visualizer:</strong>
</p>

<p align="center">
  Able to change array size, generate new arrays, and select algorithms:
</p>

<p align="center">
  <img src="https://user-images.githubusercontent.com/86130442/131289060-9d2ca6a5-ad37-464c-bcdc-fbd57ab08cdd.gif" alt="animated" />
</p>

***

<p align="center">
  <strong>Searching Visualizer:</strong>
</p>

<p align="center">
  Able to change array size, generate new arrays, sort arrays, change search term and of course, select algorithms:
</p>

<p align="center">
  <img src="https://user-images.githubusercontent.com/86130442/131287945-a9409a1d-7f8e-4396-af52-14591e421225.gif" alt="animated" />
</p>

## Performance Improvements

* Compiling with Pyinstaller
  * Up to 3x faster
* Partial Display Refresh (Only update changed pixels between frames)
  * Increased performance by ~2x (Adding nodes) to ~354x (Large maze generation)
  * A typical performance increase between ~30x to ~100x for pathfinding algorithms and medium maze generation
  * 'V' button can be used to visualize the changed squares between toggles
  * For comparison, check out archived branch [archive/V2.0/feature-complete](https://github.com/ShanaryS/algorithm-visualizer/tree/archive/V2.0/feature-complete)
* C++ Algorithms
  * 50x faster than pure python with #include algorithms.h
    * Python only interacts with C++ through thread locked Observer Pattern style calls
    * At 60fps for GUI and user input updates, limiting factor is C++ code (<10ms of 16.6ms rendering budget)
    * Above 60fps, limiting factor becomes python blocking C++ through thread locks for reading data
  * 1.6x slower than pure python with #include square.h (High overhead sending data between C++ and python up to 10kHz)
  * Nodes are flattened from 2D into a 1D Vector for cache efficiency.
  * Uses pybind11 to send data between python and C++, CMake for compiling config
  * For comparison, edit 'include_cpp.json' to switch between C++ and python
  * Current #includes shown as GUI window title

<p align="center">
  <strong>Speed up in action! (Relative to above gifs):</strong>
</p>

(Pure Python) Partial Display Refresh Speedup: | C++ Algorithms:
:-------------------------:|:-------------------------:
![Partial Display Refresh](https://user-images.githubusercontent.com/86130442/160454970-8e499a0f-32ee-4165-8376-856f05f726f1.gif)  |  ![C++ Algorithms]()
The purple color shows what pixels have been changed since the 'V' button toggle. It visualizes the per-pixel display update feature. | It may not look much faster but this is a 50x perf improvement! Notice algorithm timer in the center of the legend.


## Installation (C++20 | Python 3.10)

Clone this repo and cd into it:

```bash
git clone https://github.com/ShanaryS/algorithm-visualizer.git
cd algorithm-visualizer
```

Create and activate your virtual environment:

* Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

* MacOS/Linux:
```bash
virtualenv --no-site-packages venv
source venv/bin/activate
```

Install the required packages (While inside the virtual environment):

```bash
pip install -r requirements.txt
```

For compiling the C++ code, the CMakeLists.txt is all you need. The result will be a python extension (.pyd) in the same directory as the source files (for easy importing to python).

# Usage

To create portable .exe files for each visualizer, setup the virtual environment as described above along with installing requirements.txt (On windows just run 'create_venv.cmd').
Then simply run the 'create_exe.cmd' file. After about 2 minutes, all three visualizers will be in the newly created 'bin' folder in the root of the project.
The script will attempt to sign the executables with microsoft's signtool if a valid certificate is available. You can create a valid self signed certificate by following [this guide](https://stackoverflow.com/a/47144138).

Or run each visualizer directly using:

* Pathfinding Visualizer:
```bash
python run_pathfinding_visualizer
```

* Sorting Visualizer:
```bash
python run_sorting_visualizer
```

* Searching Visualizer:
```bash
python run_searching_visualizer
```

To use google maps functionality, you need static maps api key from google.

You can get it for free at: https://developers.google.com/maps/documentation/maps-static/get-api-key.

Once you have access, create a '.env' file in the lib directory (also for .exe) with the text:
```bash
API_KEY="YOUR_KEY"
```
Replace YOUR_KEY with your key.

## License
[MIT](https://github.com/ShanaryS/algorithm-visualizer/blob/main/LICENSE)
