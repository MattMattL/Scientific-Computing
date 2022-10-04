'''
Scientific Computing - Source Control

Started:    19 Oct 2021
Due:        01 Nov 2021

This code is for visualising randomly generated particles and their nearest
neighbours. Visualisation is done by drawing a circle with r=0 centred around
each particle and increasing the radius until it touches another particle, which
is the nearest particle to the centre particle. A line is then plotted to the
nearest particle, directly showing the nearest neighbour of all particles.
'''

import numpy as np
import matplotlib as plt
from mpl_toolkits import mplot3d

from search import *


''' Constants '''

# Adjust the constants to simulate random points in different settings

NUM_POINTS = 20 # the number of random points to be generated
DIMENSION = 3 # currently only supports 2D and 3D plots
RANDOM_SEED = 1234


''' Function Definition '''

# ONLY_FOR() is used to execute dimension-specific code. If the pre-generated
# points are 3D, only the second line is executed:
#
#   DIMENSION = 3
#   if ONLY_FOR(2): (draw a 2D plot)  <- not executed
#   if ONLY_FOR(3): (draw a 3D plot)  <- executed
# 
def ONLY_FOR(dimension):
    return dimension == DIMENSION

# FOR() is used to execute dimension-specific code that also depends on its
# sub-dimensions. For example, when initialising y-axis properties, the x-axis
# can be initialised together without a huge mess, helping possible future
# extensions (although it has a due date) for 1D or 4D plots
#
#   DIMENSION = 2
#   if FOR(1): (set x axis)  <- executed
#   if FOR(2): (set y axis)  <- executed
#   if FOR(3): (set z axis)  <- not executed
# 
def FOR(dimension):
    return dimension <= DIMENSION

# returns the Pythagoras distance between two points.
# hard-coded to eliminate for-loops for speed (there are only 2 cases)
def distance(p1, p2):
    if len(p1) == 2:
        return np.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)
    elif len(p1) == 3:
        return np.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2 + (p2[2]-p1[2])**2)

    return 0


''' Code '''

# exit if the dimension is not supported
if DIMENSION != 2 and DIMENSION != 3:
    print("Dimension not supported")
    exit()

# generate random points and find their nearest neighbour
point_cloud = generate_point_cloud(NUM_POINTS, DIMENSION, RANDOM_SEED)
nearestFrom = find_all_nearest_neighbours(point_cloud)

# declare figure and plot axes
if ONLY_FOR(2): fig, plotAxes = plt.subplots(1)

if ONLY_FOR(3): fig = plt.figure()
if ONLY_FOR(3): plotAxes = plt.axes(projection='3d')
if ONLY_FOR(3): viewingAngle = 0

# set titles
fig.canvas.set_window_title('Nearest Neighbour Visualisation')
plotAxes.set_title("{} Particles at Random Positions and Their Nearest Neighbour\
        \n(change between 2D and 3D in the code!)".format(NUM_POINTS))

# set axis labels
if FOR(1): plotAxes.set_xlabel("$x$")
if FOR(2): plotAxes.set_ylabel("$y$")
if FOR(3): plotAxes.set_ylabel("$z$")

# plot all the points and save their references to be able to change colour later
greyPoints = []

for coord in point_cloud:
    if ONLY_FOR(2): greyPoints.append(plotAxes.plot(coord[0], coord[1], color='grey', marker='o')[0])
    if ONLY_FOR(3): greyPoints.append(plotAxes.plot(coord[0], coord[1], coord[2], color='grey', marker='o')[0])

# iterate over all points
for index, coord in enumerate(point_cloud):
    # get the radius to its nearest neighbour
    nearestRadius = distance(coord, point_cloud[nearestFrom[index]])
    radius = 0
    
    # used in 3D plot to save the nearest neighbour
    bluePoint = None 

    # show current centre point as a red dot
    greyPoints[index].set_color('red')

    # draw a circle with an increasing radius to visualise the nearest particle
    while DIMENSION == 2 and radius < nearestRadius:
        redCircle = None

        # plot a circle centred around the target particle with increasing r until
        # it reaches its nearest particle
        radius += (nearestRadius-radius)/8 + 0.0001 # varying dr/dt > 0 for a better animation

        theta = np.linspace(0, 2*np.pi, 60)
        x = coord[0] + radius * np.cos(theta)
        y = coord[1] + radius * np.sin(theta)

        redCircle = plotAxes.plot(x, y, color='red', linestyle='-', linewidth=0.8)

        # reset axis limits to block the circle from overwriting the limits
        plotAxes.set_xlim(-0.1, 1.1)
        plotAxes.set_ylim(-0.1, 1.1)
        
        plt.draw()
        plt.pause(0.01)

        plotAxes.lines.remove(redCircle[0])

    # draw a sphere with an increasing radius to visualise the nearest particle
    while DIMENSION == 3 and radius < nearestRadius:
        # only remove the circle, no need to reset everything
        redSphere = []

        # plot a sphere centred around the target particle with increasing r until
        # it reaches its nearest particle
        radius += (nearestRadius-radius)/8 + 0.0001 # varying dr/dt > 0 for a better animation

        theta = np.linspace(0, np.pi, 16)
        phi = np.linspace(0, 2*np.pi, 16)

        # plot latitudinal lines (custom sphere mesh because the default functions were unsatisfactory)
        for t in theta:
            x = coord[0] + (radius * np.sin(t) * np.cos(phi))
            y = coord[1] + (radius * np.sin(t) * np.sin(phi))
            z = coord[2] + (radius * np.cos(t))

            # save to a list to be able to delete later
            redSphere.append(plotAxes.plot(x, y, z, color='red', linewidth=0.1)[0])

        # plot longitudinal lines
        for p in phi:
            x = coord[0] + (radius * np.sin(theta) * np.cos(p))
            y = coord[1] + (radius * np.sin(theta) * np.sin(p))
            z = coord[2] + (radius * np.cos(theta))

            redSphere.append(plotAxes.plot(x, y, z, color='red', linewidth=0.1)[0])

        # plot a blue dot when the sphere is close to it to show the nearest point
        if radius/nearestRadius > 0.9 and bluePoint is None:
            nearestP = point_cloud[nearestFrom[index]]
            bluePoint = plotAxes.plot(nearestP[0], nearestP[1], nearestP[2], color='blue', marker='o')

        # reset axis limits to block the sphere from overwriting the limits
        plotAxes.set_xlim(-0.1, 1.1)
        plotAxes.set_ylim(-0.1, 1.1)
        plotAxes.set_zlim(-0.1, 1.1)

        # rotate the 3D space to avoid it looking like 2D and confusing
        viewingAngle += 1 # no need to do mod(360) as the value normally doesn't get too large
        plotAxes.view_init(35 + 10*np.sin(viewingAngle/45), viewingAngle)
        
        plt.draw()
        plt.pause(0.005)

        # remove the sphere to draw another one
        for j in range(len(redSphere)):
            plotAxes.lines.remove(redSphere[j])

    # plot a line to the its nearest particle
    if FOR(1): x1, x2 = coord[0], point_cloud[nearestFrom[index], 0]
    if FOR(2): y1, y2 = coord[1], point_cloud[nearestFrom[index], 1]
    if FOR(3): z1, z2 = coord[2], point_cloud[nearestFrom[index], 2]
    
    if ONLY_FOR(2): plotAxes.plot([x1, x2], [y1, y2], color='black', linestyle='-')
    if ONLY_FOR(3): plotAxes.plot([x1, x2], [y1, y2], [z1, z2], color='black', linestyle='-')

    # update the colour of the centre point
    greyPoints[index].set_color('black')

    # remove the temporary blue dot for nearest neighbour visualisation
    if ONLY_FOR(3): plotAxes.lines.remove(bluePoint[0])

plt.draw() # to update the plot
plt.show() # to keep it on the screen
