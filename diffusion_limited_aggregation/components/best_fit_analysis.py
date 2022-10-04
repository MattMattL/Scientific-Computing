import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets

from components.component_base import ComponentBase

class BestFitAnalysis(ComponentBase, object):

    x = 0.755
    y = 0.17

    posY = 3 # y coordinate at half x range (limitX / 2)
    slope = 1.6
    limitX, limitY = 0, 0

    isLineShown = True

    def heightCallback(self, value):
        """ Slider to set the y intersect of the ruler """
        self.posY = value

        self.program.controlPanel.infoAnalysis.updateY(self.posY)
        self.program.analysisScreen.calculateError()
        self.updateLineEquation()

    def slopeCallback(self, value):
        """ Slider to set the slope of the ruler """
        self.slope = value

        self.program.controlPanel.infoAnalysis.updateSlope(self.slope)
        self.program.analysisScreen.calculateError()
        self.updateLineEquation()    

    def toggleButtonCallback(self, event):
        """ Displays/hides the ruler if clicked """
        if self.isLineShown:
            self.lineHandle.set_xdata([0, 0])
            self.lineHandle.set_ydata([0, 0])
        else:
            self.updateLineEquation()

        self.isLineShown = not self.isLineShown
        self.plt.draw()


    def yUpCallback(self, event):
        """ Button for finely adjusting the y intersect (increasing way) """
        self.posY += 0.01

        self.program.controlPanel.infoAnalysis.updateY(self.posY)
        self.program.analysisScreen.calculateError()
        self.updateLineEquation()

    def yDownCallback(self, event):
        """ Button for finely adjusting the y intersect (decreasing way) """
        self.posY -= 0.01

        self.program.controlPanel.infoAnalysis.updateY(self.posY)
        self.program.analysisScreen.calculateError()
        self.updateLineEquation()

    def slopeUpCallback(self, event):
        """ Button for finely adjusting the slope (increasing way) """
        self.slope += 0.01

        self.program.controlPanel.infoAnalysis.updateSlope(self.slope)
        self.program.analysisScreen.calculateError()
        self.updateLineEquation()

    def slopeDownCallback(self, event):
        """ Button for finely adjusting the slope (decreasing way) """
        self.slope -= 0.01

        self.program.controlPanel.infoAnalysis.updateSlope(self.slope)
        self.program.analysisScreen.calculateError()
        self.updateLineEquation()


    def leftWindowCallback(self, percentage):
        """ Sets the left windowing limit in terms of percentage """
        self.program.analysisScreen.setLeftWindow(percentage)

    def rightWindowCallback(self, percentage):
        """ Sets the right windowing limit in terms of percentage """
        self.program.analysisScreen.setRightWindow(percentage)


    def __init__(self, program, plt):
        # initialise the parent class
        super(BestFitAnalysis, self).__init__(program, plt)

        # save frequently used objects locally
        self.program = program
        self.plt = plt
        self.plotAxes = self.program.analysisScreen.axes

        # add initial plot and save the returned object
        dummy = [0, 0]
        self.lineHandle, = self.plotAxes.plot(dummy, dummy, color='black', linestyle='-', linewidth=0.5, label="best fit line")

        ''' Group Panel and Title '''

        # initialise group panel and set the title
        self.groupAxes = self.addGroupPanel([self.x, self.y, 0.24, 0.51])
        self.addGroupTitle(self.groupAxes, "6.2. Best Fit Analysis", (0.03, 0.93))

        ''' Sliders for error windowing '''

        self.addAnnotation("Error Windowing", (0.03, 0.85))

        pos = [self.x+0.03, self.y+0.39, 0.16, 0.02]
        self.leftWindowHandle = self.addSlider(pos, "L", 0, 100, 0, "%.0f%%", self.leftWindowCallback)

        pos = [self.x+0.03, self.y+0.35, 0.16, 0.02]
        self.rightWindowHandle = self.addSlider(pos, "R", 0, 100, 100, "%.0f%%", self.rightWindowCallback)

        ''' Sliders for course adjustments '''

        self.addAnnotation("Course Adjustment", (0.03, 0.61))

        # sliders for adjusting best line fit
        pos = [self.x+0.03, self.y+0.27, 0.16, 0.02]
        self.heightSliderHandle = self.addSlider(pos, "y ", 1, 7, self.posY, "%.1f", self.heightCallback)

        pos = [self.x+0.03, self.y+0.23, 0.16, 0.02]
        self.slopeSliderHandle = self.addSlider(pos, r"$\frac{dy}{dx}$ ", 1, 2.5, self.slope, "%.1f", self.slopeCallback)

        # toggle button for showing/hiding a best fit line
        pos = [self.x+0.016, self.y+0.01, 0.08, 0.05]
        self.toggleButtonHandle = self.addButton(pos, "Show/Hide", self.toggleButtonCallback)

        ''' Buttons for fine adjustments '''

        self.addAnnotation("Fine Adjustment", (0.03, 0.35))

        buttonX, buttonY = 0.025, 0.045
        
        pos = [self.x+0.076, self.y+0.12, buttonX, buttonY]
        self.yUpHandle = self.addButton(pos, "△", self.yUpCallback)
        self.addAnnotation("$y+0.01$", (0.07, 0.27))

        pos = [self.x+0.076, self.y+0.07, buttonX, buttonY]
        self.yDownHandle = self.addButton(pos, "▽", self.yDownCallback)
        self.addAnnotation("$y-0.01$", (0.07, 0.17))

        pos = [self.x+0.106, self.y+0.12, buttonX, buttonY]
        self.slopeUpHandle = self.addButton(pos, "▵", self.slopeUpCallback)
        self.addAnnotation("$y'+0.01$", (0.59, 0.27))

        pos = [self.x+0.106, self.y+0.07, buttonX, buttonY]
        self.slopeDownHandle = self.addButton(pos, "▿", self.slopeDownCallback)
        self.addAnnotation("$y'-0.01$", (0.59, 0.17))

    def updateLineEquation(self):
        """ Re-calculates the best fit line equation and plots it """

        # calculate the line equation using the current settings
        halfX = self.limitX / 2

        coordX = [-5, self.limitX+5]
        coordY = [self.slope * (-5 - halfX) + self.posY, self.slope * (5 + halfX) + self.posY]

        # plot the line
        self.lineHandle.set_xdata(coordX)
        self.lineHandle.set_ydata(coordY)

        self.plt.draw()

    def setXLim(self, x):
        self.limitX = x

    def setYLim(self, y):
        self.limitY = y

    def getY(self, x):
        return self.slope * (x - self.limitX/2) + self.posY
