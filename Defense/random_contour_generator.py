#region Story:
# I am trying to generate an image of a random contour using python but I couldn't find an easy way to do it.
# Initially I thought of doing it using matplotlib and gaussian functions, but I could not even get close to
# the image I showed.
# Is there a simple way to do it?
# I appreciate any help
#endregion

#region Solution:

#region matplotlib Path
# A simple way to achieve random and quite smoothed shapes is using matplotlib.path module.
# Using a cubic Bézier curve, most of the lines will be smoothed, and the number of sharp edges will be one
# of the parameters to tune.
# The steps would be the following.
# First the parameters of the shape are defined, these are the number of sharp edges n and
# the maximum perturbation with respect to the default position in the unit circle r.
# In this example, the points are moved from the unit circle with a radial correction, which modifies the radius
# from 1 to a random number between 1-r,1+r.
# That is why the vertices are defined as sinus or cosinus of the corresponding angle times the radius factor,
# to place the dots in the circle and then modify their radius in order to introduce the random component.
# The stack, .T to transpose and [:,None] are merely to convert the arrays to the input accepted by matplotlib.
# Below there is an example using this kind of radial correction:

import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import numpy as np


n = 8 # Number of possibly sharp edges
r = .7 # magnitude of the perturbation from the unit circle,
# should be between 0 and 1
N = n*3+1 # number of points in the Path
# There is the initial point and 3 points per cubic bezier curve.
# Thus, the curve will only pass though n points, which will be the sharp edges,
# the other 2 modify the shape of the bezier curve

angles = np.linspace(0,2*np.pi,N)
codes = np.full(N,Path.CURVE4)
codes[0] = Path.MOVETO

verts = np.stack((np.cos(angles),np.sin(angles))).T*(2*r*np.random.random(N)+1-r)[:,None]
verts[-1,:] = verts[0,:] # Using this instad of Path.CLOSEPOLY avoids an innecessary straight line
path = Path(verts, codes)

fig = plt.figure()
ax = fig.add_subplot(111)
patch = patches.PathPatch(path, facecolor='none', lw=2)
ax.add_patch(patch)

ax.set_xlim(np.min(verts)*1.1, np.max(verts)*1.1)
ax.set_ylim(np.min(verts)*1.1, np.max(verts)*1.1)
# ax.axis('off') # removes the axis to leave only the shape

# fig.canvas.draw()
# plt.show()
#endregion

#region Gaussian filtered matplotlib Path
# There is also the option of generating the shape with the code above for a single shape, and then
# use scipy to performe a gaussian filtering of the generated image.
# The main idea behind performing a gaussian filter and retrieving the smoothed shape is to create a filled shape;
# save the image as a 2d array (whose values will be between 0 and 1 as it will be a greyscale image);
# then apply the gaussian filter; and eventually, get the smoothed shape as the 0.5 contour of the filtered array.
# Therefore, this second version would look like:

# additional imports
from skimage import color as skolor # see the docs at scikit-image.org/
from skimage import measure
from scipy.ndimage import gaussian_filter

sigma = 7 # smoothing parameter
# ...
path = Path(verts, codes)

ax = fig.add_axes([0,0,0.5,0.5]) # create the subplot filling the whole figure
patch = patches.PathPatch(path, facecolor='k', lw=2) # Fill the shape in black
# ...
# ax.axis('off')

fig.canvas.draw()
plt.show()

##### Smoothing ####
# get the image as an array of values between 0 and 1
# data = data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
gray_image = skolor.rgb2gray(data)

# filter the image
smoothed_image = gaussian_filter(gray_image,sigma)

# Retrive smoothed shape as 0.5 contour
# smooth_contour = measure.find_contours(smoothed_image[::-1,:], 0.5)[0]
smooth_contour = measure.find_contours(smoothed_image[::-1,:], 0.5)
# Note, the values of the contour will range from 0 to smoothed_image.shape[0]
# and likewise for the second dimension, if desired,
# they should be rescaled to go between 0,1 afterwards

# compare smoothed ans original shape
fig = plt.figure(figsize=(8,4))
ax1 = fig.add_subplot(1,2,1)
patch_1 = patches.PathPatch(path, facecolor='none', lw=2)
ax1.add_patch(patch_1)
ax1.set_xlim(np.min(verts)*1.1, np.max(verts)*1.1)
ax1.set_ylim(np.min(verts)*1.1, np.max(verts)*1.1)
ax.axis('on')   # ax1.axis('off') # removes the axis to leave only the shape
ax2 = fig.add_subplot(1,2,2)
ax2.plot(smooth_contour[:1], smooth_contour[:0], linewidth=2, c='k')
# ax2.axis('off')

fig.canvas.draw()
plt.show()
#endregion

#endregion