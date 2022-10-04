import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets

from components.component_base import ComponentBase

class ModeControl(ComponentBase, object):

    x = 0.005
    y = 0.01

    ''' Call back functions for selecting mode '''

    def controlModeCallback(self, event):
        """ Displays control screen and updates the axes """
        self.program.plotScreen.showScreen()
        self.program.analysisScreen.hideScreen()
        self.program.controlPanel.infoAnalysis.updatePlotDescription("$-y$ versus $x$\n")
        self.plt.draw()

    def analysisModeCallback(self, event):
        """ Displays analysis screen and updates the axes """
        self.program.plotScreen.hideScreen()
        self.program.analysisScreen.showScreen()
        self.program.controlPanel.infoAnalysis.updatePlotDescription("$log$(# of Particles within Radius)\n        versus $log$(Radius)")
        self.plt.draw()

    def __init__(self, program, plt):
        # initialise the parent class
        super(ModeControl, self).__init__(program, plt)

        # save frequently used objects locally
        self.program = program
        self.plt = plt

        # declare the group panel
        self.groupAxes = self.addGroupPanel([self.x, self.y, 0.24, 0.07])

        # add buttons for selecting mode
        width = 0.1
        height = 0.05

        self.d = self.addButton([self.x+0.01, self.y+0.01, width, height], "Lattice Mode", self.controlModeCallback)
        self.a = self.addButton([self.x+width+0.03, self.y+0.01, width, height], "Analysis Mode", self.analysisModeCallback)
