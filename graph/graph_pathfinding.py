import pygame
from node import Square
from queue import PriorityQueue
import random
import time


'''
New features for the future:

Update only affect nodes rather than entire screen to improve performance (currently very good already)
    Especially when drawing lines. Currently creating mid and large graphs is slow
Instantly update algo when draw wall after completion, much like dragging nodes
Add prim maze and sticky mud


Bugs to fix:

When clicking to remove start/end node with mid node and reinstating it on completed algo, doesn't update properly
Bi-directional dijkstra only draws best_path when edges of swarms are touching. Only manifests with mid nodes
Maze can change size if window loses focus for a few seconds. Mainly with the large maze.
    pygame.event.set_grab prevents mouse from leaving window but also prevents exists
    pygame.mouse.get_focused() potential elegant solution
'''




# For use in draw() function
square_color, square_pos = square.draw_square()


def draw_square(square_color, square_pos):
    pygame.draw.rect(WINDOW, square_color, square_pos)
