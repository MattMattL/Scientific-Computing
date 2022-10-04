import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets

class InformationPanel():

    # updates the number of plotting points displayed on the screen
    def updateNumPoints(self):
        # remove the old value
        self.annNumPoints.remove()

        # format and add the new value on the screen
        formatted = "#Points = " + str(self.interface.plotScreen.numPoints)
        self.annNumPoints = self.infoAxes.annotate(formatted, xy=(0.01, 0.5), xycoords='axes fraction', color='white')

    # updates Nyquist frequency displayed on the screen
    def updateNyquist(self):
        # remove the old value
        self.annNyquist.remove()

        # calculate and add updated Nyquist frequency on the screen
        numPoints = self.interface.plotScreen.numPoints
        maxTime = self.interface.plotScreen.maxTime

        formatted = "Nyquist = {:3.0f}".format(2*numPoints / maxTime)
        self.annNyquist = self.infoAxes.annotate(formatted, xy=(0.3, 0.5), xycoords='axes fraction', color='white')

    def __init__(self, interfaceIn, plt):
        # save frequently used objects locally
        self.interface = interfaceIn
        self.plt = plt

        # declare an axes for the information panel (above the main screen)
        self.infoAxes = self.plt.axes([0.05, 0.87, 0.4, 0.08], facecolor=[0, 0, 0])
        self.infoAxes.get_xaxis().set_visible(False)
        self.infoAxes.get_yaxis().set_visible(False)

        # save variables used below (too long to write every time)
        numPoints = self.interface.plotScreen.numPoints
        maxTime = self.interface.plotScreen.maxTime

        # add the initial annotation for the # of points and save it to delete later
        formatted = "#Points = " + str(numPoints)
        self.annNumPoints = self.infoAxes.annotate(formatted, xy=(0.01, 0.5), xycoords='axes fraction', color='white')

        # add the initial annotation for Nyquist frequency and save it to delete later
        formatted = "Nyquist = {:3.0f}$/s$".format(2*numPoints / maxTime)
        self.annNyquist = self.infoAxes.annotate(formatted, xy=(0.3, 0.5), xycoords='axes fraction', color='white')