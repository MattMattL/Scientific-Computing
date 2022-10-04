'''
Module      Scientific Computing
Project     Free falling object with a = -1 m/s^2

Started     5 October 2021
Deadline    18 October 2021

    Description
Plots a graph

    Files
- freefall.py
'''

import numpy as np
import matplotlib.pyplot as plt
import math

# updates the bar graphs for pos, vel and acc. called every dt
def updateBarProperties(axes, valueX, xlim, ylim, title):
    axes.set_title(title)
    axes.set_xlim(xlim[0], xlim[1])
    axes.set_ylim(ylim[0], ylim[1])
    axes.set_xticks([]) # hide numbers along the x-axis
    axes.set_xlabel(valueX)

# updates the main plot. called every dt
def updateGraphProperties(axes, xlabel, ylabel, xlim, ylim, title):
    axes.set_title(title)
    axes.set_xlim(xlim[0], xlim[1])
    axes.set_ylim(ylim[0], ylim[1])
    axes.set_xlabel(xlabel)
    axes.set_ylabel(ylabel)

# constants
INITIAL_HEIGHT = 100 # (m)
ACCELERATION = -1 # (m/s^2)
dt = 0.079 # (s) set to an awkward number to get more decimal points in the result

EXPECTED_TIME_TAKE = math.sqrt(2 * INITIAL_HEIGHT / abs(ACCELERATION))
BAR_COLOUR = (0.5, 0.2, 0.8)

# variables
position = INITIAL_HEIGHT
velocity = 0

# arrays for plotting the main graph
arrTime = [0]
arrHeight = [INITIAL_HEIGHT]

# 4  axes for the main graph, pos, vel and acc
fig, axes = plt.subplots(1, 4, gridspec_kw={'width_ratios': [6, 1, 1, 1]})
plotAxes, posAxes, velAxes, accAxes = axes
fig.canvas.set_window_title('Free Falling')

# hide y-axis lable and ticks of the bar graphs
posAxes.yaxis.set_visible(False)
velAxes.yaxis.set_visible(False)
accAxes.yaxis.set_visible(False)

while arrHeight[-1] > 0:
    # clear previous plots
    plotAxes.clear()
    posAxes.clear()
    velAxes.clear()
    accAxes.clear()

    # reset axes properties (removed by the clear() command)
    updateGraphProperties(plotAxes, "time / $s$", "height / $m$", [0, 15], [0, 110], "Height of a free falling object on the moon\nversus time")
    updateBarProperties(posAxes, "{0:.1f} $m$".format(position), [0, 1], [0, 110], "pos")
    updateBarProperties(velAxes, "{0:.1f} $m/s$".format(velocity), [0, 1], [0, 14.13], "vel")
    updateBarProperties(accAxes, "{0:.0f} $m/s^2$".format(ACCELERATION), [0, 1], [0, 2], "acc")

    # update variables using Newton's equation of motion
    velocity += ACCELERATION * dt
    position += velocity * dt

    # save new values into arrays for the main plot
    arrTime.append(arrTime[-1] + dt)
    arrHeight.append(position)

    # re-plot
    plotAxes.plot(arrTime, arrHeight)
    posAxes.bar(0.5, position, 1, color=BAR_COLOUR)
    velAxes.bar(0.5, abs(velocity), 1, color=BAR_COLOUR)
    accAxes.bar(0.5, abs(ACCELERATION), 1, color=BAR_COLOUR)

    # print time taken so far
    formatted = '$t = {0:.3f}$'.format(arrTime[-1])
    plotAxes.annotate(formatted, xy=(0.75, 0.95), fontsize=10, xycoords='axes fraction')

    # print expected time taken to reach the ground
    formatted = 'expected $t = {0:.3f}$'.format(EXPECTED_TIME_TAKE)
    plotAxes.annotate(formatted, xy=(0.02, 0.95), fontsize=10, xycoords='axes fraction')

    '''
    Small difference between 't' and 'expected t' is from the fact that it is
    not possible to set the variable 'dt' infinitely small
    '''

    # print the plot and pause so it is actually showing up
    plt.draw()
    plt.pause(0.001)

# 'show' to keep it on the screen 
plt.show()
