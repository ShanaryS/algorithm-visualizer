# Algorithm Visualizer

This tool visualizes the operations of the most popular pathfinding, sorting, and searching algorithms. This is helpful to anyone trying to understand these algorithms or even just to enjoy the beauty of math. This was implemented fully using NumPy and Matplotlib for Search and Sort visualizations, and Pygame with google maps API for pathfinding visualizations. All done in Python, fully interactive for all algorithms with multithreading/multiprocessing support and per pixel screen updates.

***

<p align="center">
  <strong>Pathfinding Visualizer:</strong> <a href="https://replit.com/@ShanaryS/Pathfinding-Visualizer?v=1">Try it Online!</a>
</p>

<p align="center">
  Able to draw custom walls and drag nodes after algorithm completion:
</p>

<p align="center">
  <img src="https://user-images.githubusercontent.com/86130442/132488928-2ddace80-7be9-404d-903e-ecfe360bbf7f.gif" alt="animated" />
</p>

***

<p align="center">
  Visit the streets of anywhere in the world! Powered by google maps API:
</p>

<p align="center">
  <img src="https://user-images.githubusercontent.com/86130442/135311945-822a86b2-e09a-480d-bd98-c21d604a2f8f.gif" alt="animated" />
</p>

Add mid node to layer the search! Able to drag mid node as well:             |  Generate mazes with recursive division animations or instantly:
:-------------------------:|:-------------------------:
![Pathfinding Demo #2](https://user-images.githubusercontent.com/86130442/132563386-554f632d-e1bf-41f8-9e5d-1f6e06487186.gif)  |  ![Pathfinding Demo #3](https://user-images.githubusercontent.com/86130442/132563681-c7387b5b-f8b3-4e7b-9578-34428a0f850c.gif)

***

<p align="center">
  <strong>Sorting Visualizer:</strong> <a href="https://replit.com/@ShanaryS/Sorting-Visualizer?v=1">Try it Online!</a>
</p>

<p align="center">
  Able to change array size, generate new arrays, and select algorithms:
</p>

<p align="center">
  <img src="https://user-images.githubusercontent.com/86130442/131289060-9d2ca6a5-ad37-464c-bcdc-fbd57ab08cdd.gif" alt="animated" />
</p>

***

<p align="center">
  <strong>Searching Visualizer:</strong> <a href="https://replit.com/@ShanaryS/Searching-Visualizer?v=1">Try it Online!</a>
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
* Partial display update (Only update changed pixels between frames; Took a lot of effort!)
  * Increased performance by ~2x (Adding nodes) to ~354x (Large maze generation)
  * A typical performance increase between ~30x to ~100x for pathfinding algorithms and medium maze generation
  * 'V' button can be used to visualize the changed squares between toggles
  * For comparison, check out archived branch [archive/V2.0/entire-display-update](https://github.com/ShanaryS/algorithm-visualizer/tree/archive/V2.0/entire-display-update)

## Installation (Python 3.9.9)

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

# Usage

To create portable .exe files for each visualizer, setup the virtual environment as described above along with installing requirements.txt (On windows just run 'create_venv.bat').
Then simply run the 'create_exe.bat' file. After about 2 minutes, all three visualizers will be in the newly created 'bin' folder in the root of the project.

Or run each visualizer directly using:

* Pathfinding Visualizer:
```bash
python run_pathfinding_visualizer
```

* Sort Visualizer:
```bash
python run_sort_visualizer
```

* Search Visualizer:
```bash
python run_search_visualizer
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
