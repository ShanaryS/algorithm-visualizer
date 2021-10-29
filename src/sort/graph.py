"""Draws and updates graph for visualization"""


from src.sort.colors import *
from dataclasses import dataclass
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider
from src.sort import algorithms as sort
from src.sort.values import generate_array, remove_duplicates


@dataclass
class Graph:
    """Contains current state of graph"""

    array: any
    array_size: int
    labels: list[int]  # Name of xaxis values. Setting to index of array.
    is_sorted: bool

    vis: plt.bar  # Object that contains the graph
    pause_short: float  # Sets pause length for visualizations. Relative to size.
    pause_mid: float  # Needed for some algos
    pause_long: float  # Longer pause that is needed for certain visualizations
    # Change update_pause() function if changing formula for pause


def set_graph(g: Graph) -> None:
    """Creates graph. Gets called each time it updates"""

    # Clears previous graph for update
    plt.clf()
    g.vis = plt.bar(g.labels, g.array, color=DEFAULT)
    plt.subplots_adjust(left=0.15, bottom=0.3)

    # Shows 'x', 'y' or 'xy' axis
    show_axis()

    # Creates buttons and sliders used for interacting with graph. Must be done after axis.
    buttons_sliders(g)


def buttons_sliders(g: Graph) -> None:
    """Handles buttons and sliders to display on the graph"""

    # Creates buttons with their locations, text, and color
    generate_loc = plt.axes([0.35, 0.235, 0.3, 0.05])  # left, bottom, width, height
    generate = Button(ax=generate_loc, label='Generate New Array', color=CYAN)
    stop_loc = plt.axes([0.85, 0.03, 0.1, 0.05])  # left, bottom, width, height
    stop = Button(ax=stop_loc, label='Stop', color=RED)
    size_loc = plt.axes([0.05, 0.235, 0.05, 0.5])
    size = Slider(ax=size_loc, label='Size & Speed', valmin=5, valmax=100,
                  valinit=g.array_size, valstep=1, orientation='vertical')
    sel_loc = plt.axes([0.225, 0.03, 0.15, 0.05])
    sel = Button(ax=sel_loc, label='Selection', color=ORANGE)
    ins_loc = plt.axes([0.625, 0.1, 0.15, 0.05])
    ins = Button(ax=ins_loc, label='Insertion', color=ORANGE)
    bub_loc = plt.axes([0.425, 0.03, 0.15, 0.05])
    bub = Button(ax=bub_loc, label='Bubble', color=ORANGE)
    heap_loc = plt.axes([0.225, 0.1, 0.15, 0.05])
    heap = Button(ax=heap_loc, label='Heapsort', color=YELLOW)
    quick_loc = plt.axes([0.625, 0.17, 0.15, 0.05])
    quick = Button(ax=quick_loc, label='Quicksort', color=GREEN)
    merge_loc = plt.axes([0.225, 0.17, 0.15, 0.05])
    merge = Button(ax=merge_loc, label='Mergesort', color=GREEN)
    tim_loc = plt.axes([0.425, 0.1, 0.15, 0.05])
    tim = Button(ax=tim_loc, label='Timsort', color=GREEN)
    radix_loc = plt.axes([0.425, 0.17, 0.15, 0.05])
    radix = Button(ax=radix_loc, label='Radix', color=GREEN)
    bogo_loc = plt.axes([0.625, 0.03, 0.15, 0.05])
    bogo = Button(ax=bogo_loc, label='Bogosort', color=TOMATO)

    # These functions define the action on click
    def generate_new_array(_) -> None:
        g.array = generate_array(0, 150, g.array_size)
        set_graph(g)
        g.is_sorted = False
        generate.disconnect(generate_cid)

    def stop_graph(_) -> None:
        plt.close()
        set_graph(g)
        g.is_sorted = True
        stop.disconnect(stop_cid)

    def change_size(_) -> None:
        g.array_size = int(size.val)
        update_array(g)
        g.is_sorted = False

    def sel_sort(_) -> None:
        if g.is_sorted:
            update_array(g)
        g.is_sorted = True
        sort.selection(g.vis, g.array, g.array_size, g.pause_short, g.pause_mid)
        sel.disconnect(sel_cid)

    def ins_sort(_) -> None:
        if g.is_sorted:
            update_array(g)
        g.is_sorted = True
        sort.insertion(g.vis, g.array, g.array_size, g.pause_short)
        ins.disconnect(ins_cid)

    def bub_sort(_) -> None:
        if g.is_sorted:
            update_array(g)
        g.is_sorted = True
        sort.bubble(g.vis, g.array, g.array_size, g.pause_short)
        bub.disconnect(bub_cid)

    def heap_sort(_) -> None:
        if g.is_sorted:
            update_array(g)
        g.is_sorted = True
        sort.heap(g.vis, g.array, g.array_size, g.pause_short, g.pause_long)
        heap.disconnect(heap_cid)

    def quick_sort(_) -> None:
        if g.is_sorted:
            update_array(g)
        g.is_sorted = True
        sort.quick(g.vis, g.array, g.array_size, g.pause_short)
        quick.disconnect(quick_cid)

    def merge_sort(_) -> None:
        if g.is_sorted:
            update_array(g)
        g.is_sorted = True
        sort.merge(g.vis, g.array, g.array_size, g.pause_short)
        merge.disconnect(merge_cid)

    def tim_sort(_) -> None:
        if g.is_sorted:
            update_array(g)
        g.is_sorted = True
        sort.tim(g.vis, g.array, g.array_size, g.pause_short)
        tim.disconnect(tim_cid)

    def radix_sort(_) -> None:
        if g.is_sorted:
            update_array(g)
        g.is_sorted = True
        delete_duplicates(g)
        sort.radix(g.vis, g.array, g.array_size, g.pause_short, g.pause_long)
        radix.disconnect(radix_cid)

    def bogo_sort(_) -> None:
        if g.is_sorted:
            update_array(g)
        g.is_sorted = True
        sort.bogo(g.vis, g.array, g.array_size, g.pause_short)
        bogo.disconnect(bogo_cid)

    # These allow resetting the button after click, allowing repeat clicks
    generate_cid = generate.on_clicked(generate_new_array)
    stop_cid = stop.on_clicked(stop_graph)
    size.on_changed(change_size)
    sel_cid = sel.on_clicked(sel_sort)
    ins_cid = ins.on_clicked(ins_sort)
    bub_cid = bub.on_clicked(bub_sort)
    heap_cid = heap.on_clicked(heap_sort)
    quick_cid = quick.on_clicked(quick_sort)
    merge_cid = merge.on_clicked(merge_sort)
    tim_cid = tim.on_clicked(tim_sort)
    radix_cid = radix.on_clicked(radix_sort)
    bogo_cid = bogo.on_clicked(bogo_sort)

    # Displays the graph. plt.show() should only be ran once with plt.draw() used for updates. But doesn't work.
    plt.show()


def update_array(g: Graph) -> None:
    """Used for updating slider of array size"""

    g.array = generate_array(0, 150, g.array_size)
    g.labels = [label for label in range(g.array_size)]
    update_pause(g)
    set_graph(g)


def delete_duplicates(g: Graph) -> None:
    """Removes duplicates in array"""

    g.array = remove_duplicates(g.array)
    g.array_size = len(g.array)
    g.labels = [label for label in range(g.array_size)]
    update_pause(g)
    set_graph(g)


def update_pause(g) -> None:
    """Updates pause values"""

    g.pause_short = 150 / g.array_size * 0.01
    g.pause_mid = (g.pause_short * 3) + (g.array_size * 0.001)
    g.pause_long = (g.pause_short * 3) + (g.array_size * 0.005)


def show_axis(axis: str = 'None') -> None:
    """Enable showing x and y axis"""

    if axis == 'None':
        plt.axis('off')
    elif axis == 'x':
        plt.axis('on')
        plt.gca().axes.xaxis.set_visible(True)
        plt.gca().axes.yaxis.set_visible(False)
    elif axis == 'y':
        plt.axis('on')
        plt.gca().axes.xaxis.set_visible(True)
        plt.gca().axes.xaxis.set_visible(False)
    elif axis == 'xy':
        plt.axis('on')
        plt.gca().axes.xaxis.set_visible(True)
        plt.gca().axes.xaxis.set_visible(True)
