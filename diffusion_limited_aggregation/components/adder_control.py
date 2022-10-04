import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets

from components.component_base import ComponentBase

import time

class AdderControl(ComponentBase, object):

    addPerClick = 10

    x = 0.005 # x offset of the group panel
    y = 0.09 # y offset of the group panel

    def numberSliderCallback(self, val):
        """ Updates the number of points to be added per add-button click """
        self.addPerClick = int(val)
        self.plt.draw()

    def addButtonCallback(self, event):
        """ Adds and plots each point by calling other classes """

        # show that it is calculating and not crashed
        self.annotHandle.set(text="Calculating...")
        self.plt.pause(0.001)

        executionTime = time.time()

        for _ in range(self.addPerClick):
            # add a new particle and save the coordinates returned
            x, y = self.program.lattice.add()

            # call the plot function and pass the coordinates
            self.program.plotScreen.addParticleAt(x, y)

        executionTime = time.time() - executionTime
        print("{0:.3f} s".format(executionTime))

        # update plot properties
        self.program.plotScreen.updateAxisLimits()
        self.program.analysisScreen.updatePlot()
        self.annotHandle.set(text="")
        self.plt.draw()

    def __init__(self, program, plt):
        # initialise the parent class
        super(AdderControl, self).__init__(program, plt)

        # save frequently used objects locally
        self.program = program
        self.plt = plt

        ''' Group Panel and Annotations '''

        # add a group panel and set the title
        self.groupAxes = self.addGroupPanel([self.x, self.y, 0.24, 0.11])
        self.addGroupTitle(self.groupAxes, "5. Run", (0.03, 0.72))

        # annotation to show the program is still running and not crashed
        self.annotHandle = self.addAnnotation("", (0.55, 0.7))

        ''' Sliders and Buttons '''

        # add a slider for choosing the number of particles to add per click
        pos = [self.x+0.08, self.y+0.02, 0.12, 0.02]
        self.sliderAxes, self.sliderHandle = self.addSlider(pos, "# ", 1, 3000, self.addPerClick, "%3d", self.numberSliderCallback)

        # add a button for adding particles
        pos = [self.x+0.01, self.y+0.01, 0.04, 0.05]
        self.buttonAxes, self.buttonHandle = self.addButton(pos, "add", self.addButtonCallback)
