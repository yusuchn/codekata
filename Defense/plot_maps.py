import matplotlib
# set matplotlib to use 'TKAgg' would make the plot to be in a seperate figure outside the IDE
# rather than in "ScieView" to the right side of the IDE, in the "Plots" pane
matplotlib.use('TKAgg')

import matplotlib.pyplot as plt
# from matplotlib.path import Path
# import matplotlib.patches as patches
# import numpy as np

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
