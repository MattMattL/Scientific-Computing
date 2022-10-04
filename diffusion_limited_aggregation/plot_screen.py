import numpy as np
import matplotlib.pyplot as plt

class PlotScreen:

    plotHandle = []

    firstR, firstG, firstB = 1, 0, 0
    secondR, secondG, secondB = 0, 0, 1

    plotCount = 0

    def __init__(self, program, ptl):
        # save frequently used objects locally
        self.program = program
        self.plt = plt

        # initialise plot axes
        self.axes = self.plt.axes([0.25, 0, 0.5, 1])

        # set axis limits and direction
        self.updateAxisLimits()

        # plot initial seed
        self.addSeedAt(0, 0)

    def _getNextSingleColour(self, first, second):
        # returns the next R, G or B value.
        # sine & cosine functions are to gradually alternate between two preset R,G or B values

        if first > second:
            return abs(first - second) * (np.cos(self.plotCount/1024)/2 + 0.5) + min(first, second)
        else:
            return abs(first - second) * (np.sin(self.plotCount/1024)/2 + 0.5) + min(first, second)

    def _getNextRGB(self):
        # returns the next RGB value in a list
        
        self.plotCount += 1

        return [self._getNextSingleColour(self.firstR, self.secondR), \
                self._getNextSingleColour(self.firstG, self.secondG), \
                self._getNextSingleColour(self.firstB, self.secondB)]

    def hideScreen(self):
        """ hides the screen by setting the axes size 0 x 0 """
        self.axes.set_position([0, 0, 0, 0])

    def showScreen(self):
        """ displays the screen by resetting the axes size """
        self.axes.set_position([0.25, 0, 0.5, 1])

    def reset(self):
        """ Removes all plots and resets plot handler """

        for marker in self.plotHandle:
            self.axes.lines.remove(marker)

        self.plotHandle = []

    def addSeedAt(self, x, y):
        """ Plots a seed particle at the given location """

        returned = self.axes.plot(x, y, marker='o', color='black', markersize=2)
        self.plotHandle.append(returned[0])

    def addParticleAt(self, x, y):
        """ Plots a particle at the given location """

        returned = self.axes.plot(x, y, marker='o', color=self._getNextRGB(), markersize=1)
        self.plotHandle.append(returned[0])

    def updateAxisLimits(self):
        """ Updates axis limits to be the widest view """

        limit = self.program.lattice.maxRadius + 3

        # set axis limits
        self.axes.set_xlim(-limit, limit)
        self.axes.set_ylim(-limit, limit)

        self.axes.invert_yaxis()

