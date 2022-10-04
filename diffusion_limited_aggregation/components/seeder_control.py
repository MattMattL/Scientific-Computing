import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets

from components.component_base import ComponentBase

class SeederControl(ComponentBase, object):

    x = 0.005 # x offset of the group panel
    y = 0.56 # y offset of the group panel

    isMarkerShown = False

    ''' Buttons for moving around on the map and placing seed particles '''

    pointerX, pointerY = 0, 0

    def upButtonCallback(self, event):
        self.pointerY -= 1
        self.updateCurrentPos()

    def downButtonCallback(self, event):
        self.pointerY += 1
        self.updateCurrentPos()

    def leftButtonCallback(self, event):
        self.pointerX -= 1
        self.updateCurrentPos()

    def rightButtonCallback(self, event):
        self.pointerX += 1
        self.updateCurrentPos()

    def confirmButtonCallback(self, event):
        self.program.lattice.set(self.pointerX, self.pointerY, True)
        self.program.plotScreen.addSeedAt(self.pointerX, self.pointerY)

        self.showMarker()
        self.plt.draw()


    ''' Helper functions for visualising current coordinate '''

    plotHandle = []

    def showMarker(self):
        """ Plots a marker at the current pos """

        returned = self.program.plotScreen.axes.plot(self.pointerX, self.pointerY, marker='+', color='blue', markersize=12)
        self.plotHandle.append(returned[0])
        
        self.isMarkerShown = True
        self.plt.draw()

    def updateCurrentPos(self):
        """ Updates the position and re-draws the marker """
        
        self.hideMarker()

        returned = self.program.plotScreen.axes.plot(self.pointerX, self.pointerY, marker='+', color='blue', markersize=12)
        self.plotHandle.append(returned[0])

        self.isMarkerShown = True
        self.plt.draw()

    def hideMarker(self):
        """ Hides all markers """

        for marker in self.plotHandle:
            self.program.plotScreen.axes.lines.remove(marker)

        self.isMarkerShown = False
        self.plotHandle = []
        self.plt.draw()

    def toggleMarkerCallback(self, event):
        """ Toggles the marker on and off """

        if self.isMarkerShown:
            self.hideMarker()
        else:
            self.showMarker()


    def __init__(self, program, plt):
        # initialise the parent class
        super(SeederControl, self).__init__(program, plt)

        # save frequently used objects locally
        self.program = program
        self.plt = plt

        ''' Group Panel and Annotations '''

        # initialise group panel and set the title
        self.groupAxes = self.addGroupPanel([self.x, self.y, 0.24, 0.2])
        self.addGroupTitle(self.groupAxes, "2. Seed Particles Initialisation", (0.03, 0.86))

        ''' Arrows and Confirm buttons '''

        # pre-calculate button location, offset and size
        centreX, centreY = self.x + 0.04, self.y + 0.06
        offsetX, offsetY = 0.45/16, 0.45/9
        buttonX, buttonY = 0.4/16, 0.4/9

        # upward button
        pos = [centreX, centreY+offsetY, buttonX, buttonY]
        self.upButtonAxes, self.upButtonHandle = self.addButton(pos, "△", self.upButtonCallback)

        # downward button
        pos = [centreX, centreY-offsetY, buttonX, buttonY]
        self.downButtonAxes, self.downButtonHandle = self.addButton(pos, "▽", self.downButtonCallback)

        # leftward button
        pos = [centreX-offsetX, centreY, buttonX, buttonY]
        self.leftButtonAxes, self.leftButtonHandle = self.addButton(pos, "◁", self.leftButtonCallback)

        # rightward button
        pos = [centreX+offsetX, centreY, buttonX, buttonY]
        self.rightButtonAxes, self.rightButtonHandle = self.addButton(pos, "▷", self.rightButtonCallback)

        # confirm button
        pos = [centreX, centreY, buttonX, buttonY]
        self.confirmButtonAxes, self.confirmButtonHandle = self.addButton(pos, "+", self.confirmButtonCallback)

        ''' Buttons for other seeder settings '''

        # show/hide button
        pos = [self.x+0.14, centreY, 0.08, buttonY]
        self.toggleButtonAxes, self.toggleButtonHandle = self.addButton(pos, "Show/Hide", self.toggleMarkerCallback)
