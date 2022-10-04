import numpy as np
import matplotlib.pyplot as plt

class AnalysisScreen:

    MAX_RADIUS = 1000

    # array for saving the number of particles with radius in range [i, i+1)
    countsPerRadius = [0] * MAX_RADIUS

    maxX = 0;
    arrX = [0]
    cumulativeCounts = [0]

    leftPercentage, rightPercentage = -1000, -1000
    leftLimit, rightLimit = -10, 1000

    def __init__(self, program, ptl):
        # save frequently used objects locally
        self.program = program
        self.plt = plt

        # initialise plot axes (initially hidden)
        self.axes = self.plt.axes([0, 0, 0, 0])

        # initialise plot axes and save it to update the values later
        self.plotHandle, = self.axes.plot(self.arrX, self.cumulativeCounts, color='red', marker='.', markersize=3, linestyle='', label="particle count")

        # initialise lines for windowing limits
        self.leftWindowHandle, = self.axes.plot([-10, -10], [-5, 20], color='black', linewidth=0.5, linestyle='--', label="windowing limits")
        self.rightWindowHandle, = self.axes.plot([-10, -10], [-5, 20], color='black', linewidth=0.5, linestyle='--')

        # set axis limits
        self.axes.set_xlim(([0, 0.5]))
        self.axes.set_ylim(([0, 0.5]))

    def registerRadius(self, radius):
        """ Increases the counter at index = int(radius) by one """
        self.countsPerRadius[int(radius)] += 1

    def hideScreen(self):
        """ hides the screen by setting the axes size 0 x 0 """
        self.axes.set_position([0, 0, 0, 0])

    def showScreen(self):
        """ displays the screen by resetting the axes size """

        # update the plot
        self.updatePlot()

        # reset the axes size to display the plot
        self.axes.set_position([0.29, 0.1, 0.44, 0.8])

    def updatePlot(self):
        # find the last non-zero index from dataset (is also the x range)
        lastNonZeroIndex = len(self.countsPerRadius) - 1

        while self.countsPerRadius[lastNonZeroIndex] == 0 and lastNonZeroIndex > 0:
            lastNonZeroIndex -= 1

        nonZeroSize = lastNonZeroIndex + 1

        # exit if there is no data to plot
        if lastNonZeroIndex < 1:
            return

        # generate an array for the x values (radius)
        self.arrX = [i for i in range(nonZeroSize)]

        # calculate cumulative radius count (y values)
        count = 0
        self.cumulativeCounts = [0] * (nonZeroSize)

        for i in range(nonZeroSize):
            count += self.countsPerRadius[i]
            self.cumulativeCounts[i] = count

        # decide plotting scale and frequency
        self.arrX = np.log(self.arrX[1::])
        self.cumulativeCounts = np.log(self.cumulativeCounts[1::])

        # plot the number of particles with radius <= r versus r
        self.plotHandle.set_xdata(self.arrX)
        self.plotHandle.set_ydata(self.cumulativeCounts)

        # update windowing limits
        self.setLeftWindow(self.leftPercentage)
        self.setRightWindow(self.rightPercentage)

        # set axis limits
        self.maxX = self.arrX[-1]
        self.axes.set_xlim([0, self.maxX + 0.5])
        self.axes.set_ylim([0, self.cumulativeCounts[-1] + 0.5])

        # pass limits to draw the best fit line
        bestFitLine = self.program.controlPanel.bestFitAnalysis

        bestFitLine.setXLim(self.maxX)
        bestFitLine.setYLim(self.cumulativeCounts[-1])

        bestFitLine.updateLineEquation()

    def setLeftWindow(self, percentage):
        self.leftPercentage = percentage
        self.leftLimit = self.maxX * percentage / 100

        self.leftWindowHandle.set_xdata([self.leftLimit, self.leftLimit])

        self.calculateError()
        self.plt.draw()

    def setRightWindow(self, percentage):
        self.rightPercentage = percentage
        self.rightLimit = self.maxX * percentage / 100

        self.rightWindowHandle.set_xdata([self.rightLimit, self.rightLimit])
        
        self.calculateError()
        self.plt.draw()

    def calculateError(self):
        validPosX = []
        ssr = 0
        ess = 0

        line = self.program.controlPanel.bestFitAnalysis

        # find Sum Square Risidual (sum of delta y squared)
        for i, x in enumerate(self.arrX):
            if self.leftLimit <= x <= self.rightLimit:
                ssr += (self.cumulativeCounts[i] - line.getY(x)) ** 2
                validPosX.append(x)

        # exit if athere are less tha 2 points available (gradient cannot be calculated)
        if len(validPosX) < 3:
            self.program.controlPanel.infoAnalysis.updateError(0)
            return

        ssr /= len(validPosX) - 2

        # find Explained Sum Squared
        averageX = sum(validPosX) / len(validPosX)

        ess = sum([(x - averageX)**2 for x in validPosX])

        # update the error in gradient
        self.program.controlPanel.infoAnalysis.updateError(np.sqrt(ssr / ess))
