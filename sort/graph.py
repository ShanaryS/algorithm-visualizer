"""Draws and updates graph for visualization"""


import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider
from sort import algorithms as sort
from sort.colors import *
from sort.values import generate_array, remove_duplicates


# Base variables
array = generate_array(0, 150, 30)
array_size: int = len(array)
labels: list[int] = [label for label in range(array_size)]         # Name of xaxis values. Setting to index of array.
is_sorted: bool = False

vis: plt.bar = None                                              # Object that contains the graph
pause_short: float = 150 / array_size * 0.01                   # Sets pause length for visualizations. Relative to size.
pause_mid: float = (pause_short * 3) + (array_size * 0.001)    # Needed for some algos
pause_long: float = (pause_short * 3) + (array_size * 0.005)   # Longer pause that is needed for certain visualizations
# Change update_pause() function if changing formula for pause


def set_graph() -> None:
    """Creates graph. Gets called each time it updates"""

    # Clears previous graph for update
    plt.clf()
    global vis
    vis = plt.bar(labels, array, color=MPL_DEFAULT)
    plt.subplots_adjust(left=0.15, bottom=0.3)

    # Shows 'x', 'y' or 'xy' axis
    show_axis()

    # Creates buttons and sliders used for interacting with graph. Must be done after axis.
    buttons_sliders()


def buttons_sliders() -> None:
    """Handles buttons and sliders to display on the graph"""

    global array_size

    # Creates buttons with their locations, text, and color
    generate_loc = plt.axes([0.35, 0.235, 0.3, 0.05])  # left, bottom, width, height
    generate = Button(ax=generate_loc, label='Generate New Array', color=MPL_CYAN)
    stop_loc = plt.axes([0.85, 0.03, 0.1, 0.05])  # left, bottom, width, height
    stop = Button(ax=stop_loc, label='Stop', color=MPL_RED)
    size_loc = plt.axes([0.05, 0.235, 0.05, 0.5])
    size = Slider(ax=size_loc, label='Size & Speed', valmin=5, valmax=100,
                  valinit=array_size, valstep=1, orientation='vertical')
    sel_loc = plt.axes([0.225, 0.03, 0.15, 0.05])
    sel = Button(ax=sel_loc, label='Selection', color=MPL_ORANGE)
    ins_loc = plt.axes([0.625, 0.1, 0.15, 0.05])
    ins = Button(ax=ins_loc, label='Insertion', color=MPL_ORANGE)
    bub_loc = plt.axes([0.425, 0.03, 0.15, 0.05])
    bub = Button(ax=bub_loc, label='Bubble', color=MPL_ORANGE)
    heap_loc = plt.axes([0.225, 0.1, 0.15, 0.05])
    heap = Button(ax=heap_loc, label='Heapsort', color=MPL_YELLOW)
    quick_loc = plt.axes([0.625, 0.17, 0.15, 0.05])
    quick = Button(ax=quick_loc, label='Quicksort', color=MPL_GREEN)
    merge_loc = plt.axes([0.225, 0.17, 0.15, 0.05])
    merge = Button(ax=merge_loc, label='Mergesort', color=MPL_GREEN)
    tim_loc = plt.axes([0.425, 0.1, 0.15, 0.05])
    tim = Button(ax=tim_loc, label='Timsort', color=MPL_GREEN)
    radix_loc = plt.axes([0.425, 0.17, 0.15, 0.05])
    radix = Button(ax=radix_loc, label='Radix', color=MPL_GREEN)
    bogo_loc = plt.axes([0.625, 0.03, 0.15, 0.05])
    bogo = Button(ax=bogo_loc, label='Bogosort', color=MPL_TOMATO)

    # These functions define the action on click
    def generate_new_array(_) -> None:
        global array, is_sorted
        array = generate_array(0, 150, array_size)
        set_graph()
        is_sorted = False
        generate.disconnect(generate_cid)

    def stop_graph(_) -> None:
        global is_sorted
        plt.close()
        set_graph()
        is_sorted = True
        stop.disconnect(stop_cid)

    def change_size(_) -> None:
        global array_size, is_sorted
        array_size = int(size.val)
        update_array()
        is_sorted = False

    def sel_sort(_) -> None:
        global is_sorted
        if is_sorted:
            update_array()
        is_sorted = True
        sort.selection(vis, array, array_size, pause_short, pause_mid)
        sel.disconnect(sel_cid)

    def ins_sort(_) -> None:
        global is_sorted
        if is_sorted:
            update_array()
        is_sorted = True
        sort.insertion(vis, array, array_size, pause_short)
        ins.disconnect(ins_cid)

    def bub_sort(_) -> None:
        global is_sorted
        if is_sorted:
            update_array()
        is_sorted = True
        sort.bubble(vis, array, array_size, pause_short)
        bub.disconnect(bub_cid)

    def heap_sort(_) -> None:
        global is_sorted
        if is_sorted:
            update_array()
        is_sorted = True
        sort.heap(vis, array, array_size, pause_short, pause_long)
        heap.disconnect(heap_cid)

    def quick_sort(_) -> None:
        global is_sorted
        if is_sorted:
            update_array()
        is_sorted = True
        sort.quick(vis, array, array_size, pause_short)
        quick.disconnect(quick_cid)

    def merge_sort(_) -> None:
        global is_sorted
        if is_sorted:
            update_array()
        is_sorted = True
        sort.merge(vis, array, array_size, pause_short)
        merge.disconnect(merge_cid)

    def tim_sort(_) -> None:
        global is_sorted
        if is_sorted:
            update_array()
        is_sorted = True
        sort.tim(vis, array, array_size, pause_short)
        tim.disconnect(tim_cid)

    def radix_sort(_) -> None:
        global is_sorted
        if is_sorted:
            update_array()
        is_sorted = True
        delete_duplicates()
        sort.radix(vis, array, array_size, pause_short, pause_long)
        radix.disconnect(radix_cid)

    def bogo_sort(_) -> None:
        global is_sorted
        if is_sorted:
            update_array()
        is_sorted = True
        sort.bogo(vis, array, array_size, pause_short)
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


def update_array() -> None:
    """Used for updating slider of array size"""

    global array, labels
    array = generate_array(0, 150, array_size)
    labels = [label for label in range(array_size)]
    update_pause()
    set_graph()


def delete_duplicates() -> None:
    """Removes duplicates in array"""

    global array, array_size, labels
    array = remove_duplicates(array)
    array_size = len(array)
    labels = [label for label in range(array_size)]
    update_pause()
    set_graph()


def update_pause() -> None:
    """Updates pause values"""
    global pause_short, pause_mid, pause_long
    pause_short = 150 / array_size * 0.01
    pause_mid = (pause_short * 3) + (array_size * 0.001)
    pause_long = (pause_short * 3) + (array_size * 0.005)


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
