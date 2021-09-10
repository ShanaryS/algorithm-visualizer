# Algorithm Visualizer

This is a tool to visualize the operations of the most popular pathfinding, sort, and search algorithms. This is helpful to anyone trying to understand these algorithms or even to someone who has already grasped them. This was implemented fully using NumPy and Matplotlib for Search and Sort visualizations, and Pygame for pathfinding visualizations. All done in Python, fully interactive for all algorithms.
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

Add mid node to layer the search! Able to drag mid node as well:             |  Generate mazes with recursive divison animations or instantly:
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

## Installation

Clone this repo and cd into it:

```bash
git clone https://github.com/ShanaryS/algorithm-visualizer.git
cd algorithm-visualizer
```

Create and activate your virtual environment:

* Windows:
```bash
virtualenv env
.\env\Scripts\activate
```

* MacOS/Linux:
```bash
virtualenv --no-site-packages env
source env/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

# Usage

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
