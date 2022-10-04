import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets

from lattice import Lattice
from components.component_base import ComponentBase

class PresetControl(ComponentBase, object):

    latticeSize = None

    x = 0.005 # x offset of the group panel
    y = 0.77 # y offset of the group panel

    ''' Functions for adjusting direction bias '''

    def biasRightCallback(self, val):
        self.program.lattice.setBias(val, "RIGHT")

    def biasLeftCallback(self, val):
        self.program.lattice.setBias(val, "LEFT")

    def biasUpwardCallback(self, val):
        self.program.lattice.setBias(val, "UP")

    def biasDownwardCallback(self, val):
        self.program.lattice.setBias(val, "DOWN")


    def __init__(self, program, plt):
        # initialise the parent class
        super(PresetControl, self).__init__(program, plt)

        # save frequently used objects locally
        self.program = program
        self.plt = plt

        # update local variables
        self.latticeSize = self.program.lattice.MAP_SIZE

        ''' Group Panel and Annotations '''

        # add group panel and set the title
        self.groupAxes = self.addGroupPanel([self.x, self.y, 0.24, 0.22])
        self.addGroupTitle(self.groupAxes, "1. Directional Properties", (0.03, 0.85))

        # add annotation for bias sliders
        self.addAnnotation("Relative Bias", (0.09, 0.65))

        ''' Sliders and Buttons '''

        # rightward slider
        pos = [self.x+0.025, self.y+0.105, 0.17, 0.02]
        self.biasRightAxes, self.biasRightHandle = self.addSlider(pos, "x ", 0, 2, 1, "%.2f", self.biasRightCallback)

        # leftward slider
        pos = [self.x+0.025, self.y+0.075, 0.17, 0.02]
        self.biasLeftAxes, self.biasLeftHandle = self.addSlider(pos, "-x ", 0, 2, 1, "%.2f", self.biasLeftCallback)

        # upward slider
        pos = [self.x+0.025, self.y+0.045, 0.17, 0.02]
        self.biasUpAxes, self.biasUpHandle = self.addSlider(pos, "y ", 0, 2, 1, "%.2f", self.biasUpwardCallback)

        # downward slider
        pos = [self.x+0.025, self.y+0.015, 0.17, 0.02]
        self.biasDownAxes, self.biasDownHandle = self.addSlider(pos, "-y ", 0, 2, 1, "%.2f", self.biasDownwardCallback)
