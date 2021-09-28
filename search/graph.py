"""Draws and updates graph for visualization"""


import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider, TextBox
from search import algorithms as search
from search.colors import MatplotlibColors as PltC
from search.values import generate_array, KEY


# Base variables
array = generate_array(0, 150, 30)
array_size: int = len(array)
labels: list[int] = [label for label in range(array_size)]         # Name of xaxis values. Setting to index of array.
key: int = KEY

vis: plt.bar = None                                              # Object that contains the graph
pause_short: float = 150 / array_size * 0.01                   # Sets pause length for visualizations. Relative to size.
pause_long: float = (pause_short * 3) + (array_size * 0.005)   # Longer pause that is needed for certain visualizations
HESITATE: float = 0.5                                          # Pause before starting animations
# Change update array if changing formula for pause


def set_graph(initialize=False) -> None:
    """Creates graph. Gets called each time it updates"""

    # Clears previous graph for update
    plt.clf()
    global vis
    vis = plt.bar(labels, array, color=PltC.DEFAULT)
    plt.subplots_adjust(left=0.15, bottom=0.3)

    # Shows 'x', 'y' or 'xy' axis
    show_axis()

    # Creates buttons and sliders used for interacting with graph. Must be done after axis.
    buttons_sliders(initialize=initialize)


def buttons_sliders(initialize=False) -> None:
    """Handles buttons and sliders to display on the graph"""

    global array_size, key

    # Creates buttons with their locations, text, and color
    generate_loc = plt.axes([0.2, 0.2, 0.3, 0.05])  # left, bottom, width, height
    generate = Button(ax=generate_loc, label='Generate New Array', color=PltC.CYAN)
    stop_loc = plt.axes([0.85, 0.01, 0.1, 0.05])  # left, bottom, width, height
    stop = Button(ax=stop_loc, label='Stop', color=PltC.RED)
    size_loc = plt.axes([0.05, 0.235, 0.05, 0.5])
    size = Slider(ax=size_loc, label='Size & Speed', valmin=5, valmax=100,
                  valinit=array_size, valstep=1, orientation='vertical')
    text_loc = plt.axes([0.475, 0.01, 0.3, 0.05])
    text = TextBox(ax=text_loc, label='Enter search value (1-150): ', initial=str(key))
    sort_loc = plt.axes([0.60, 0.2, 0.3, 0.05])
    sort = Button(ax=sort_loc, label='Sort Array', color=PltC.CYAN)
    binary_loc = plt.axes([0.025, 0.1, 0.15, 0.05])
    binary = Button(ax=binary_loc, label='Binary', color=PltC.GREEN)
    jump_loc = plt.axes([0.225, 0.1, 0.15, 0.05])
    jump = Button(ax=jump_loc, label='Jump', color=PltC.GREEN)
    exp_loc = plt.axes([0.425, 0.1, 0.15, 0.05])
    exp = Button(ax=exp_loc, label='Exponential', color=PltC.GREEN)
    fib_loc = plt.axes([0.625, 0.1, 0.15, 0.05])
    fib = Button(ax=fib_loc, label='Fibonacci', color=PltC.GREEN)
    linear_loc = plt.axes([0.825, 0.1, 0.15, 0.05])
    linear = Button(ax=linear_loc, label='Linear', color=PltC.YELLOW)

    # These functions define the action on click
    def generate_new_array(_) -> None:
        global array
        array = generate_array(0, 150, array_size)
        set_graph()
        generate.disconnect(generate_cid)

    def stop_graph(_) -> None:
        plt.close()
        set_graph(initialize=True)
        stop.disconnect(stop_cid)

    def change_size(_) -> None:
        global array_size
        array_size = int(size.val)
        update_array()

    def change_key(_) -> None:
        global key
        try:
            input_num = int(text.text)
            if 1 <= input_num <= 150:
                key = input_num
            else:
                key = 44
        except ValueError:
            key = 44

    def sort_array(_) -> None:
        array.sort()
        set_graph()
        sort.disconnect(sort_cid)

    def linear_search(_) -> None:
        set_graph()
        plt.pause(HESITATE)
        search.linear(vis, key, array, array_size, pause_short)
        linear.disconnect(linear_cid)

    def binary_search(_) -> None:
        array.sort()
        set_graph()
        plt.pause(HESITATE)
        search.binary(vis, key, array, array_size, pause_long)
        binary.disconnect(binary_cid)

    def jump_search(_) -> None:
        array.sort()
        set_graph()
        plt.pause(HESITATE)
        search.jump(vis, key, array, array_size, pause_short, pause_long)
        jump.disconnect(jump_cid)

    def exp_search(_) -> None:
        array.sort()
        set_graph()
        plt.pause(HESITATE)
        search.exponential(vis, key, array, array_size, pause_long)
        exp.disconnect(exp_cid)

    def fib_search(_) -> None:
        array.sort()
        set_graph()
        plt.pause(HESITATE)
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

    # Displays the graph. plt.show() should only be ran once with plt.draw() used for updates.
    if initialize:
        plt.show()
    else:
        plt.draw()


def update_array() -> None:
    """Used for updating slider of array size"""

    global array, labels, pause_short, pause_long
    array = generate_array(0, 150, array_size)
    labels = [label for label in range(array_size)]
    pause_short = 150 / array_size * 0.01
    pause_long = (pause_short * 3) + (array_size * 0.005)
    set_graph()


def show_axis(axis='None') -> None:
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
