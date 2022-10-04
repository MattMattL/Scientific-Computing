import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets

from components.component_base import ComponentBase

class ColourPaletteControl(ComponentBase, object):

    x = 0.005 # x offset of the group panel
    y = 0.38 # y offset of the group panel

    firstR, firstG, firstB = 1, 0, 0
    secondR, secondG, secondB = 0, 0, 1

    ''' Slider callbacks for choosing transition colours '''

    def firstRedCallback(self, value):
        self.firstR = value
        self.program.plotScreen.firstR = value
        self.annotHandle1.set(color=[self.firstR, self.firstG, self.firstB])

    def firstGreenCallback(self, value):
        self.firstG = value
        self.program.plotScreen.firstG = value
        self.annotHandle1.set(color=[self.firstR, self.firstG, self.firstB])

    def firstBlueCallback(self, value):
        self.firstB = value
        self.program.plotScreen.firstB = value
        self.annotHandle1.set(color=[self.firstR, self.firstG, self.firstB])


    def secondRedCallback(self, value):
        self.secondR = value
        self.program.plotScreen.secondR = value
        self.annotHandle2.set(color=[self.secondR, self.secondG, self.secondB])

    def secondGreenCallback(self, value):
        self.secondG = value
        self.program.plotScreen.secondG = value
        self.annotHandle2.set(color=[self.secondR, self.secondG, self.secondB])

    def secondBlueCallback(self, value):
        self.secondB = value
        self.program.plotScreen.secondB = value
        self.annotHandle2.set(color=[self.secondR, self.secondG, self.secondB])


    ''' Getters for external use '''

    def getColour1(self):
        return self.firstR, self.firstG, self.firstB

    def getColour2(self):
        return self.secondR, self.secondG, self.secondB


    def __init__(self, program, plt):
        # initialise the parent class
        super(ColourPaletteControl, self).__init__(program, plt)

        # save frequently used objects locally
        self.program = program
        self.plt = plt


        ''' Group Properties and Annotations '''

        # declare the group panel
        self.groupAxes = self.addGroupPanel([self.x, self.y, 0.24, 0.17])
        self.addGroupTitle(self.groupAxes, "3. Colour Palette", (0.03, 0.85))

        ''' Sliders for choosing the first colour '''

        alignX = self.x + 0.02
        alignY = self.y + 0.01

        # first Red
        pos = [alignX, alignY+0.06, 0.07, 0.02]
        self.firstRedAxes, self.firstRedHandle = self.addSlider(pos, "R ", 0, 1, 1, "%.1f", self.firstRedCallback)

        # first Green
        pos = [alignX, alignY+0.03, 0.07, 0.02]
        self.firstGreenAxes, self.firstGreenHandle = self.addSlider(pos, "G ", 0, 1, 0, "%.1f", self.firstGreenCallback)

        # first Blue
        pos = [alignX, alignY, 0.07, 0.02]
        self.firstBlueAxes, self.firstBlueHandle = self.addSlider(pos, "B ", 0, 1, 0, "%.1f", self.firstBlueCallback)

        # slider description
        self.annotHandle1 = self.addAnnotation("First", (0.17, 0.63))

        ''' Sliders for choosing the second colour '''

        alignX = self.x + 0.14
        alignY = self.y + 0.01

        # second Red
        pos = [alignX, alignY+0.06, 0.07, 0.02]
        self.secondRedAxes, self.secondRedHandle = self.addSlider(pos, "R ", 0, 1, 0, "%.1f", self.secondRedCallback)

        # second Greren
        pos = [alignX, alignY+0.03, 0.07, 0.02]
        self.secondGreenAxes, self.secondGreenHandle = self.addSlider(pos, "G ", 0, 1, 0, "%.1f", self.secondGreenCallback)

        # second Blue
        pos = [alignX, alignY, 0.07, 0.02]
        self.secondBlueAxes, self.secondBlueHandle = self.addSlider(pos, "B ", 0, 1, 1, "%.1f", self.secondBlueCallback)

        # slider description
        self.annotHandle2 = self.addAnnotation("Second", (0.64, 0.63))