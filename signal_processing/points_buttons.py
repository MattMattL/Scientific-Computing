import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets

from fourier import sinf

class PointsButtons:

    # saves the increased number of plotting points and re-draws the default sin wave
    def addPointsCallback(self, event):
        # one click increases the number of points by 10
        self.interface.plotScreen.numPoints += 10

        # re-draw the default sin wave with the new number of points
        # (rather than saving/figuring out the current function and re-calculating for it)
        maxTime = self.interface.plotScreen.maxTime
        numPoints = self.interface.plotScreen.numPoints
        self.interface.plotScreen.arrTime = np.linspace(0, maxTime, numPoints)
        self.interface.plotScreen.arrWave = sinf(self.interface.plotScreen.arrTime, 1)

        # update the plot screen
        self.interface.plotScreen.updatePlot()

    # saves the decreased number of plotting points and re-draws the default sin wave
    def removePointsCallback(self, event):
        # one click decreases the number of points by 10. minimum number of points is 20
        newNumPoints = self.interface.plotScreen.numPoints - 10
        self.interface.plotScreen.numPoints = max(20, newNumPoints)

        # re-draw the default sin wave with the new number of points
        # (rather than saving/figuring out the current function and re-calculating for it)
        maxTime = self.interface.plotScreen.maxTime
        numPoints = self.interface.plotScreen.numPoints
        self.interface.plotScreen.arrTime = np.linspace(0, maxTime, numPoints)
        self.interface.plotScreen.arrWave = sinf(self.interface.plotScreen.arrTime, 1)

        # update the plot screen
        self.interface.plotScreen.updatePlot()

    def __init__(self, interfaceIn, plt):
        self.interface = interfaceIn
        self.plt = plt

        # add a button for adding 10 plotting points and set the callback function
        self.axesUp = self.plt.axes([0.885, 0.2, 0.035, 0.08])
        self.upHandler = widgets.Button(self.axesUp, '/\\')
        self.upHandler.on_clicked(self.addPointsCallback)

        # add a button for removing 10 plotting points and set the callback function
        self.axesDown = self.plt.axes([0.885, 0.1, 0.035, 0.08])
        self.downHandler = widgets.Button(self.axesDown, '\\/')
        self.downHandler.on_clicked(self.removePointsCallback)

        # add a label above the buttons
        self.axesUp.annotate("  Adjust\n# Points", xy=(-0.3, 1.5), xycoords='axes fraction')
