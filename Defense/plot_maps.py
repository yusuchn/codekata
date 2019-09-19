import tkinter

import matplotlib
# set matplotlib to use 'TKAgg' would make the plot to be in a seperate figure outside the PyCharm IDE
# rather than in "ScieView" to the right side of the IDE - in the "Plots" pane
matplotlib.use('TKAgg')

import matplotlib.pyplot as plt
# from matplotlib.path import Path
# import matplotlib.patches as patches

from matplotlib.animation import FuncAnimation

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np
import time

from skimage.draw import random_shapes
# from skimage import color as skolor # see the docs at scikit-image.org/
# from skimage import measure
# from scipy.ndimage import gaussian_filter

from Defense import *


def display_map_images(staged_image_list_param, staged_cost_list_param):

    fig, axes = plt.subplots(nrows=2, ncols=3)
    ax = axes.ravel()

    for i, (k, v) in enumerate(staged_image_list_param.items()):

        load_success, rgb_list, image, pix = load_from_image(v)
        # We can visualize the images.
        ax[i].imshow(image)
        # k is the label for the image
        label = str.format('{}\n{}'.format(k, staged_cost_list_param[k]))
        ax[i].set_title(label)

    for a in ax:
        a.set_xticklabels([])
        a.set_yticklabels([])

    plt.show()

def realtime_display_animated_map_images(staged_image_list_param, staged_cost_list_param,
                                     plotCanvas_param, axes_param):
    while (True):
        for i, (k, v) in enumerate(staged_image_list_param.items()):
            time.sleep(2)

            axes_param.clear()
            # DO NOT USE plotCanvas.get_tk_widget().delete('all'),
            # it delete everyting but doesn't re-draw.
            # Instead, use plotCanvas.flush_events() below

            load_success, rgb_list, image, pix = load_from_image(v)
            axes_param.imshow(image)

            # k is the label for the image, display it in the title
            label = str.format('{}\n{}'.format(k, staged_cost_list_param[k]))
            axes_param.set_title(label, fontsize=8)
            axes_param.set_xticklabels([])
            axes_param.set_yticklabels([])
            axes_param.axis('off') # removes the axis to leave only the shape

            # the code below cearl out the cavas but doesn't re-draw
            plotCanvas_param.flush_events()
            plotCanvas_param.draw()
            plotCanvas_param.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


