import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider, TextBox
from values import generate_array
from colors import *
from algorithms import algos_search as search

'''
Test circular imports with vis, else pass vis as arg
Does algos need matplotlib for plt.pause?
Replace plt.pause with time.sleep()
Rename values to array
Remove array size from buttons_sliders. Seems redundant
Need to update buttons each time call set_graph? Maybe fixes dragging slider
Maybe decouple updating slide from immediately updating graph (async?)
'''

# Base variables
array = generate_array(0, 150, 30)
array_size = len(array)
labels = [label for label in range(array_size)]
key = 44

vis = None                                              # Object that contains the graph
pause_short = 150 / array_size * 0.01                   # Sets pause length for visualizations. Relative to size.
pause_long = (pause_short * 3) + (array_size * 0.005)   # Longer pause that is needed for certain visualizations
hesitate = 1                                            # Pause before starting animations


def set_graph(initialize=False):
    """Creates graph. Gets called each time it updates"""

    # Clears previous graph for update
    update_vis()

    # Shows 'x', 'y' or 'xy' axis
    show_axis()

    # Creates buttons and sliders used for interacting with graph. Must be after done after axis.
    buttons_sliders()

    # Displays the graph. plt.show() should only be ran once with plt.draw() used for updates.
    if initialize:
        plt.show()
    else:
        plt.draw()


def update_vis():
    """Updates the graph with new visualizations"""

    global vis
    plt.clf()
    vis = plt.bar(labels, array, color=MPL_DEFAULT)
    plt.subplots_adjust(left=0.15, bottom=0.3)


# noinspection PyUnboundLocalVariable
def buttons_sliders():
    """Handles buttons and sliders on the displayed on the graph"""

    # Creates buttons with their locations, text, and color
    generate_loc = plt.axes([0.2, 0.2, 0.3, 0.05])  # left, bottom, width, height
    generate = Button(ax=generate_loc, label='Generate New Array', color=MPL_CYAN)
    stop_loc = plt.axes([0.85, 0.01, 0.1, 0.05])  # left, bottom, width, height
    stop = Button(ax=stop_loc, label='Stop', color=MPL_RED)
    size_loc = plt.axes([0.05, 0.235, 0.05, 0.5])
    size = Slider(ax=size_loc, label='Size & Speed', valmin=5, valmax=100,
                  valinit=array_size, valstep=1, orientation='vertical')
    text_loc = plt.axes([0.475, 0.01, 0.3, 0.05])
    text = TextBox(ax=text_loc, label='Enter search value (1-150): ', initial=str(key))
    sort_loc = plt.axes([0.60, 0.2, 0.3, 0.05])
    sort = Button(ax=sort_loc, label='Sort Array', color=MPL_CYAN)
    binary_loc = plt.axes([0.025, 0.1, 0.15, 0.05])
    binary = Button(ax=binary_loc, label='Binary', color=MPL_GREEN)
    jump_loc = plt.axes([0.225, 0.1, 0.15, 0.05])
    jump = Button(ax=jump_loc, label='Jump', color=MPL_GREEN)
    exp_loc = plt.axes([0.425, 0.1, 0.15, 0.05])
    exp = Button(ax=exp_loc, label='Exponential', color=MPL_GREEN)
    fib_loc = plt.axes([0.625, 0.1, 0.15, 0.05])
    fib = Button(ax=fib_loc, label='Fibonacci', color=MPL_GREEN)
    linear_loc = plt.axes([0.825, 0.1, 0.15, 0.05])
    linear = Button(ax=linear_loc, label='Linear', color=MPL_GOLD)

    # These functions define the action on click
    def generate_new_array(_):  # Argument is typically called event but using _ to suppress errors
        global array
        array = generate_array(0, 150, array_size)
        set_graph()
        generate.disconnect(generate_cid)

    def stop_graph(_):
        plt.close()
        set_graph(initialize=True)
        stop.disconnect(stop_cid)

    def change_size(_):
        global array_size
        array_size = int(size.val)
        update_array()

    def change_key(_):
        global key
        try:
            input_num = int(text.text)
            if 1 <= input_num <= 150:
                key = input_num
            else:
                key = 44
        except ValueError:
            key = 44

    def sort_array(_):
        array.sort()
        set_graph()
        sort.disconnect(sort_cid)

    def linear_search(_):
        set_graph()
        plt.pause(hesitate)
        search.linear(vis, key, array, array_size, pause_short)
        linear.disconnect(linear_cid)

    def binary_search(_):
        array.sort()
        set_graph()
        plt.pause(hesitate)
        search.binary(vis, key, array, array_size, pause_long)
        binary.disconnect(binary_cid)

    def jump_search(_):
        array.sort()
        set_graph()
        plt.pause(hesitate)
        search.jump(vis, key, array, array_size, pause_short, pause_long)
        jump.disconnect(jump_cid)

    def exp_search(_):
        array.sort()
        set_graph()
        plt.pause(hesitate)
        search.exponential(vis, key, array, array_size, pause_long)
        exp.disconnect(exp_cid)

    def fib_search(_):
        array.sort()
        set_graph()
        plt.pause(hesitate)
        search.fibonacci(vis, key, array, array_size, pause_long)
        fib.disconnect(fib_cid)

    # These allow resetting the button after click, allowing repeat clicks
    generate_cid = generate.on_clicked(generate_new_array)
    stop_cid = stop.on_clicked(stop_graph)
    size.on_changed(change_size)
    text.on_submit(change_key)
    sort_cid = sort.on_clicked(sort_array)
    linear_cid = linear.on_clicked(linear_search)
    binary_cid = binary.on_clicked(binary_search)
    jump_cid = jump.on_clicked(jump_search)
    exp_cid = exp.on_clicked(exp_search)
    fib_cid = fib.on_clicked(fib_search)


def show_axis(axis='None'):
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


def update_array():
    """Used for updating slider of array size"""

    global array, array_size, labels, pause_short, pause_long
    array = generate_array(0, 150, array_size)
    labels = [label for label in range(array_size)]
    pause_short = 150 / array_size * 0.01
    pause_long = (pause_short * 3) + (array_size * 0.005)
    set_graph()
